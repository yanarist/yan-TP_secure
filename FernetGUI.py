import logging
import base64
import hashlib
import dearpygui.dearpygui as dpg
from chat_client import ChatClient
from generic_callback import GenericCallback
from CipheredGUI import *

from cryptography.fernet import Fernet


class FernetGUI(CipheredGUI):

    def run_chat(self, sender, app_data) -> None:
    # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connexion {name}@{host}:{port}")
        
        # Utilisation de sha256().digest() et de base64.b64encode() pour la dérivation de la clef
        key_bytes = hashlib.sha256(password.encode()).digest()
        key = base64.b64encode(key_bytes)
        self._key = key
        
        self._callback = GenericCallback()
        
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)
        
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, message) -> bytes:
        # Créer un objet Fernet avec la clé de chiffrement
        fernet_object = Fernet(self._key) 
        # Convertir le message en bytes
        message_bytes = bytes(message, 'utf-8') 
        # Chiffrer le message avec l'objet Fernet
        encrypted_message = fernet_object.encrypt(message_bytes)
        # Enregistrer un message de log
        self._log.info(f"Message chiffré : {message_bytes}")
        # Retourner le message chiffré
        return (encrypted_message)
    
    def decrypt(self, message_data) -> str :
        encrypted_message = base64.b64decode(message_data['data']) 
        # Créer un objet Fernet avec la clé de chiffrement
        fernet_object = Fernet(self._key)
        # Déchiffrer le message avec l'objet Fernet
        decrypted_message = fernet_object.decrypt(encrypted_message).decode('utf8')
        # Enregistrer un message de log
        self._log.info(f"Message déchiffré : {decrypted_message}")
        # Retourner le message déchiffré
        return decrypted_message




if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()