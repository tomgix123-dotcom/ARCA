import hashlib
import config
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


#=====================HASH PARA CONTRASEÑAS==============================================
def crear_hash(texto):
    return hashlib.sha256(texto.encode()).hexdigest()
   

def check_hash(contraseña, hash, Event=None):
    if contraseña == hash:
        return True
    return False
    
#========================================================================================

#====================GENERAR SALT Y ENCRIPTADO============================================


def generar_salt():
    return os.urandom(16)


def generar_llave(contraseña,salt):

    kdf=PBKDF2HMAC( algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000)

    return kdf.derive(contraseña.encode())


def cifrar_bytes(zip_bytes,llave):

    iv=os.urandom(12)

    aes=AESGCM(llave)

    bytes_cifrados=aes.encrypt(iv,zip_bytes,None)

    return iv, bytes_cifrados



def descifrar_bytes(datos_cifrados,iv,llave):

    aes=AESGCM(llave)

    bytes_descifrados=aes.decrypt(iv,datos_cifrados,None)

    return bytes_descifrados





