import argparse
import hashlib
import hmac
import math
import re
import os

from datetime import datetime as tiempo
from cripta import Cripta as AES


"""
PROBLEMA:
Crear un programa que permita registrar una clave inicial y genere una contraseña nueva cada vez que se solicite.
Puede utilizarse cualquier librería que no sea TOTP (es decir, que no haga el trabajo sucio).
"-g": recibe un fichero con una clave hexadecimal de 64 caracteres mínimo y la guarda en un fichero "ft_otp.key".
"-k": recibe un fichero cifrado (como "ft_otp.key") y genera una contraseña temporal, mostrándola por pantalla.
El fichero "ft_otp.key" siempre estará cifrado.
"""


# ----------------------------------------------------------------------------------------------------------------------


# Leer los argumentos de entrada de la línea de comandos.
def leer_argumentos():
    # Inicializar el analizador de argumentos.
    analizador = inicializar_analizador()

    return analizador.g, analizador.k


# Inicializar el parser de la línea de comandos.
def inicializar_analizador():
    # Analizador de argumentos de la línea de comandos.
    analizador = argparse.ArgumentParser(
        # prog="./ft_otp",
        description="Herramienta casera para generar contraseñas TOTP.",
        epilog="Ejercicio 'ft_otp' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).",
    )

    # Agregar las opciones del comando.
    analizador.add_argument(
        "-g",
        metavar="fichero",
        help="almacena una clave hexadecimal de 64 caracteres mínimo en un fichero 'ft_otp.key'.",
        type=str)
    analizador.add_argument(
        "-k",
        metavar="fichero",
        help="genera una contraseña temporal usando un fichero y la muestra por pantalla.",
        type=str)
    # analizador.add_argument(
    #     "-t",
    #     metavar="segundos",
    #     help="indica el tiempo de caducidad de las contraseñas generadas.",
    #     default=int)

    # Obtener los argumentos de la línea de comandos.
    return analizador.parse_args()


# Verifica que un fichero contiene una clave que cumple los requisitos mínimos.
def validar_fichero(fichero):
    global clave

    # El fichero existe y es legible.
    if not (os.path.isfile(fichero) or os.access(fichero, os.R_OK)):
        print("Error: El fichero no existe o no es legible.")

        return False

    # Extraer clave del interior del fichero.
    with open(fichero, "r") as f:
        clave = f.read()

    # Verifica que la clave es hexadecimal y mide al menos 64 caracteres.
    if not re.match(r'^[0-9a-fA-F]{64,}$', clave):
        print("La clave no es hexadecimal o tiene menos de 64 caracteres.")

        """
        Expresión regular:
        ^           : límite inicial de la acotación de la cadena.
        [0-9a-fA-F] : cualquier caracter hexadecimal (números, o letras desde 'a' hasta 'f' o desde 'A' hasta 'F').
        {64,}       : cuantificador que indica longitud de 64 hasta ilimitados caracteres.
        $           : límite final de la acotación de la cadena.
        """

        return False

    return True


# Generar una contraseña temporal usando una clave secreta hexadecimal.
# - secreto: clave hexadecimal secreta de la que extraer un OTP.
def generar_OTP(secreto):
    # Obtener y truncar el tiempo actual a una ventana de 30 segundos.
    tiempo_actual = math.floor(tiempo.now().timestamp() / 30)

    # Generar el hash de la clave secreta (bytes).
    hashbytes = hmac.digest(secreto.encode(), str(tiempo_actual).encode(), hashlib.sha1)

    # Obtener el offset.
    offset = hashbytes[19] & 15

    # Obtener el valor de la contraseña.
    contra = 0
    contra |= (hashbytes[offset] & 15) << 24
    contra |= (hashbytes[offset + 1] & 255) << 16
    contra |= (hashbytes[offset + 2] & 255) << 8
    contra |= (hashbytes[offset + 3] & 255)

    # TODO: explicar el proceso anterior.

    # Obtener el valor de la contraseña.
    contra = (contra & 0x7FFFFFFF) % 1000000

    return contra


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos.
    fichero_clave_compartida, fichero_cifrado = leer_argumentos()

    # Si se solicitó generar una clave (-g).
    if fichero_clave_compartida and validar_fichero(fichero_clave_compartida):
        # Almacenar la clave en un fichero '.key'.
        with open("ft_otp.key", "w") as f:
            f.write(clave)

        print("Clave almacenada en 'ft_otp.key'.")

        try:
            # Cifrar el fichero con la clave.
            AES().cifrar_fichero("ft_otp.key")

            print("Fichero 'ft_otp.key' cifrado con contraseña.")

        except Exception as e:
            print("Error: " + str(e))

    # Si se solicitó generar una contraseña (-k).
    elif fichero_cifrado:
        # TODO: Generar una contraseña temporal.
        pass
    