import qrcode_terminal
import argparse
import hashlib
import struct
import hmac
import time
import re
import os

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

    return analizador.g, analizador.k, analizador.qr


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
    analizador.add_argument(
        "-qr",
        metavar="fichero",
        help="muestra un QR con la clave secreta.",
        type=str)

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


# Generar un código temporal usando una clave secreta hexadecimal.
# - secreto: clave hexadecimal secreta de la que extraer un OTP.
def generar_OTP(clave):

    # Codificar la clave hexadecimal en una cadena de bytes.
    clave_b = bytes.fromhex(clave)

    # Obtener y truncar el tiempo actual a una "ventana" de 30 segundos.
    tiempo = int(time.time() // 30)

    # Codificar el tiempo en una cadena de bytes.
    tiempo_b = struct.pack(">Q", tiempo)

    # Generar el hash de la clave secreta (como cadena de bytes).
    hash_b = hmac.digest(clave_b, tiempo_b, hashlib.sha1)

    # Obtener el offset.
    offset = hash_b[19] & 15    # Operación AND entre '0b????' y '0b1111'.

    # Generar el código.
    codigo = struct.unpack('>I', hash_b[offset:offset + 4])[0]
    codigo = (codigo & 0x7FFFFFFF) % 1000000

    # TODO: explicar el proceso anterior.

    # Devolver los 6 primeros dígitos del código.
    return "{:06d}".format(codigo)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos.
    fichero_clave_compartida, fichero_cifrado, qr = leer_argumentos()

    # Si se solicitó generar una clave (-g).
    if fichero_clave_compartida:
        if validar_fichero(fichero_clave_compartida):   # No uso AND con la de arriba para que detecte error con '-g'
            # Almacenar la clave en un fichero '.key'.
            with open("ft_otp.key", "w") as f:
                f.write(clave)

            print("Clave almacenada en 'ft_otp.key'.")

            # Cifrar el fichero con la clave.
            AES().cifrar_fichero("ft_otp.key")

            print("Fichero 'ft_otp.key' cifrado con contraseña.")

        else:
            # Los errores del fichero de la clave se tratan en 'validar_fichero()'.
            exit(1)


    # Si se solicitó generar un código temporal (-k) o mostrar el QR de la clave (-qr).
    elif fichero_cifrado or qr:
        # Usar el fichero recibido por una de las dos opciones.
        fichero = fichero_cifrado if fichero_cifrado else qr    # El fichero usado es el mismo, pero no se recibe igual

        # Verificar que el fichero cifrado existe y es legible.
        if not (os.path.isfile(fichero) or os.access(fichero, os.R_OK)):
            print("Error: El fichero no existe o no es legible.")

            exit(1)

        else:
            # Extraer la clave del interior del fichero.
            clave = AES().leer_fichero(fichero)

            # Si se solicitó generar una contraseña (-k).
            if fichero_cifrado:
                # Generar y mostrar el código OTP.
                print("Código generado:", generar_OTP(clave))

            # Si se solicitó generar un QR (-qr).
            else:
                # Generar y mostrar el QR.
                print("QR con la clave secreta:")
                qrcode_terminal.draw(clave)

    else:
        print("No se ha especificado ninguna opción.")
        exit(1)
