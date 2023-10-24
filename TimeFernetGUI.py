import logging
import base64
from FernetGUI import *
import time
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

# Time To Live en secondes
TTL = 30


class TimeFernetGUI(FernetGUI):
    def encrypt(self, string_message) -> bytes:
        # Créer un objet Fernet avec la clé de chiffrement
        fernet_object = Fernet(self._key)  
        # Récupérer le temps actuel converti en entier
        time = int(time.time())  
        # Convertir le message en bytes
        bytes_message = string_message.encode('utf-8') 
        # Chiffrer le message avec un TTL de 30 secondes
        encrypted_message = fernet_object.encrypt_at_time(bytes_message, time + TTL)  
        # Retourner le message chiffré sous forme de bytes
        return encrypted_message 


    def decrypt(self, tuple_message) -> str:
        # Récupérer le deuxième élément du tuple contenant le message à décrypter
        encrypted_message = base64.b64decode(tuple_message[1]['data'])
        # Créer un objet Fernet avec la clé de chiffrement
        fernet_object = Fernet(self._key)
        # Récupérer le temps actuel converti en entier
        temps = int(time.time())
        try:
            # Déchiffrer le message en utilisant la méthode decrypt_at_time de Fernet
            decrypted_message_bytes = fernet_object.decrypt_at_time(encrypted_message, TTL, temps)
            # Convertir le message en string
            decrypted_message = str(decrypted_message_bytes,'utf-8')
        # Si le message est expiré ou si la clé est invalide, on affiche un message d'erreur
        except InvalidToken:
            error_message = "Erreur de déchiffrement : le message a dépassé la durée de vie TTL"
            # Enregistrer le message d'erreur
            self._log.error(error_message)
        # Retourner le message déchiffré
        return decrypted_message

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()
