import logging
import base64
import dearpygui.dearpygui as dpg
from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import *
import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Cipher block (chiffrage)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.backends import default_backend

# Taille de la clé en octets
KEY_SIZE = 16 
# Nombre d'itérations pour la dérivation de la clé
ITERATIONS = 32000
# Taille d'un bloc de chiffrement en bits
BLOCK_SIZE = 128 
# Sel utilisé pour la dérivation de la clé
SALT = b"sel_derivation"



class CipheredGUI(BasicGUI):

    # Surcharge du constructeur pour y inclure le champ self._key qui contiendra la clef de chiffrement (default : None)
    def __init__(self) -> None:
        super().__init__() # Hérédité issue de la class BasicGUI
        self._key = None 

    # Surcharge de la fonction _create_connection_window() pour y inclure un champ password
    def _create_connection_window(self) -> None:
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):

            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(
                        default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            # Inclusion du champ password
            with dpg.group(horizontal=True):
                dpg.add_text("password")
                dpg.add_input_text(default_value="", tag=f"connection_password", password=True)
            dpg.add_button(label="Connect", callback=self.run_chat)


    # Surcharger la fonction run_chat() pour y inclure la récupération du password
    def run_chat(self, sender, app_data) -> None:
            # callback used by the connection windows to start a chat session
            host = dpg.get_value("connection_host")
            port = int(dpg.get_value("connection_port"))
            name = dpg.get_value("connection_name")
            self._log.info(f"Connexion {name}@{host}:{port}")

            # Introduire un mot de passe
            password = dpg.get_value("connection_password")

            
            # Dérivation de clef stockée dans self._key 
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=KEY_SIZE,
                salt=SALT,
                iterations=ITERATIONS,
                backend=default_backend()
            )
            key = kdf.derive(bytes(password, "utf8"))
            self._key = key
    
            self._callback = GenericCallback()
    
            self._client = ChatClient(host, port)
            self._client.start(self._callback)
            self._client.register(name)
    
            dpg.hide_item("connection_windows")
            dpg.show_item("chat_windows")
            dpg.set_value("screen", "Connecting")

    # Créer une fonction encrypt(), prenant une string "message" et retournant un typle de bytes (iv, encrypted)
    def encrypt(self, string_message):
        # Convertir la chaîne de caractères "message" en octets
        bytes_message = string_message.encode('utf-8')
        # Ajouter un padding pour prendre en compte les cas où la taille du message initial n'est pas un multiple de 16 octets
        padder = padding.PKCS7(BLOCK_SIZE).padder()
        padded_text = padder.update(bytes_message) + padder.finalize()
        # Générer un vecteur d'initialisation aléatoire
        iv  = os.urandom(KEY_SIZE)
        # Initialiser le cipher avec l'algorithme AES et le mode CTR
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv),backend=default_backend())
        # Initialiser l'objet encryptor avec le cipher
        encryptor = cipher.encryptor()
        # Chiffrer le message en utilisant l'encryptor
        encrypted = encryptor.update(padded_text) + encryptor.finalize()
        # Retourner le vecteur d'initialisation et le cipher final
        return (iv, encrypted)
        
    # Créer une fonction decrypt(), prenant un tuple "message" en paramètre et retournant une string utf8
    def decrypt(self, tuple_message):
        # Récupérer le premier élément du tuple contenant le vecteur d'initialisation
        iv = base64.b64decode(tuple_message[0]['data'])
        # Récupérer le deuxième élément du tuple contenant le message à décrypter
        encrypted_message = base64.b64decode(tuple_message[1]['data'])
        # Initialiser l'objet decryptor avec l'algorithme AES et le mode CTR
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv),backend=default_backend())
        # Initialiser l'objet decryptor avec le cipher
        decryptor = cipher.decryptor()
        # Déchiffrer le message
        data = decryptor.update(encrypted_message) + decryptor.finalize()
        # Retirer le padding
        unpadder = padding.PKCS7(BLOCK_SIZE).unpadder() 
        unpadder_text = (unpadder.update(data) + unpadder.finalize())
        # Convertir le message en chaîne de caractères
        decrypted = str(unpadder_text, "utf-8")
        # Retourner le message déchiffré
        return (decrypted)


    #Surcharger les fonctions send()/recv() pour y faire intervenir encrypt() et decrypt()
    
    def recv(self) -> None:
        # function called to get incoming messages and display them
        if self._callback is not None:
            for user, message in self._callback.get():
                decrypted_message = self.decrypt(message) # Déchiffrer le message reçu
                self.update_text_screen(f"{user} : {decrypted_message}")
            self._callback.clear()

    def send(self, message: str) -> None:
        # function called to send a message to all (broadcasting)
        encrypted_message = self.encrypt(message) # Chiffrer le message à envoyer
        self._client.send_message(encrypted_message)
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()