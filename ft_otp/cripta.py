from getpass import getpass
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


"""
Código rescatado y modificado del repositorio de la asignatura 'Seguridad de la Información':
https://github.com/15Galan/asignatura-303 ; Tema 2 ; Práctica 2.
"""


# Implementación básica de cifrado/descifrado usando AES en modo CBC.
class Cripta:

    # Datos necesarios
    CLAVE = None
    IV = None
    BLOQUE = None

    # Constructor de la clase
    def __init__(self):
        # self.CLAVE = get_random_bytes(16)   # Clave aleatoria: 128 bits
        # self.IV = get_random_bytes(16)      # IV aleatorio: 128 bits para CBC
        self.IV = "cb71De88D9ab1640".encode("utf-8")
        self.BLOQUE = 16  # Tamaño de bloque: 128 bits

        """
        El cifrado AES en modo CBC requiere: una clave (contraseña), un vector de
        inicialización ("semilla") y un tamaño de bloque, todos de tamaños de 16 bytes.
        
        Para la simulación de este ejercicio, el IV se dispondrá en claro para que sea constante entre instancias,
        solicitando únicamente una contraseña al usuario para acceder al contenido en claro de los ficheros.
        """

    # Cifra un texto usando AES en modo CBC con vector de inicialización IV.
    def cifrar(self, texto_claro):
        # Pedir una clave al usuario.
        self.CLAVE = getpass("Introduce una clave: ").encode("utf-8")

        # Validar longitud de la clave.
        if len(self.CLAVE) != 16:
            raise Exception("La clave debe tener 16 bytes (caracteres).")

        # Mecanismo de cifrado.
        cifrador = AES.new(self.CLAVE, AES.MODE_CBC, self.IV)

        # Cifrado haciendo que los mensajes sean múltiplo del tamaño de bloque
        return cifrador.encrypt(pad(texto_claro.encode("utf-8"), self.BLOQUE))

    # Descifra un texto cifrado usando AES en modo CBC con un vector de inicialización IV.
    def descifrar(self, texto_oculto):
        # Pedir una clave al usuario.
        self.CLAVE = getpass("Introduce la clave: ").encode("utf-8")

        # Validar longitud de la clave.
        if len(self.CLAVE) != 16:
            raise Exception("La clave debe tener 16 bytes (caracteres).")

        # Mecanismo de descifrado.
        descifrador = AES.new(self.CLAVE, AES.MODE_CBC, self.IV)

        # Desciframos, eliminamos el padding, y recuperamos la cadena
        return unpad(descifrador.decrypt(texto_oculto), self.BLOQUE).decode("utf-8", "ignore")

    # Cifra un fichero usando AES en modo CBC con un vector de inicialización IV.
    def cifrar_fichero(self, fichero):
        # Leer el contenido del fichero.
        with open(fichero, "r") as f:
            contenido = f.read()

        # Cifrar el contenido.
        oculto = self.cifrar(contenido)

        # Escribir el contenido (cifrado) en el fichero (bytes).
        with open(fichero, "wb") as f:
            f.write(oculto)

        # Texto escrito en el fichero.
        return oculto

    # Descifra un fichero usando AES en modo CBC con un vector de inicialización IV.
    def descifrar_fichero(self, fichero):
        # Leer el contenido del fichero (bytes).
        with open(fichero, "rb") as f:
            contenido = f.read()

        # Descifrar el contenido del fichero.
        claro = self.descifrar(contenido)

        # Escribir el contenido (en claro) en el fichero.
        with open(fichero, "w") as f:
            f.write(claro)

        # Texto escrito en el fichero.
        return claro

    # Lee el contenido de un fichero cifrado.
    def leer_fichero(self, fichero):
        # Leer el contenido del fichero.
        with open(fichero, "rb") as f:
            contenido = f.read()

        # Descifrar el contenido del fichero.
        claro = self.descifrar(contenido)

        # Texto escrito en el fichero.
        return claro
