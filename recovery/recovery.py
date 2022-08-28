"""
Crear un programa que, dado un rango de fechas, sea capaz de extraer diversa información
de un sistema Windows como la actividad del usuario, los programas abiertos, el historial
de navegación, distinta información del registro de Windows... en dicho rango de tiempo.

El programa recibirá un rango de fechas y mostrará por consola una lista ordenada de ficheros,
directorios y programas abiertos en dicho rango de tiempo.

Usará el módulo 'argparse' para recibir los parámetros de entrada.
"""

import win32com.client
import argparse
import datetime
import logging
import winreg
import wmi
import os

from browser_history import get_history


# ----------------------------------------------------------------------------------------------------------------------


def leer_argumentos():
    """
    Lee los argumentos de entrada de la línea de comandos.

    :return: Valor y opciones de los argumentos leídos.
    """

    # Crear un analizador de argumentos.
    analizador = argparse.ArgumentParser(
        description='Programa para obtener información de un sistema Windows.',
        epilog="Ejercicio 'recovery' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga)."
    )

    # Agregar las opciones al comando.

    # Fecha de inicio: si no se especifica, se toma la fecha timestamp 0.
    analizador.add_argument(
        '-i',
        metavar='inicio',
        help="Fecha inicial del rango de fechas en formato 'DD-MM-AAAA' (por defecto, '01-01-1970')."
    )

    # Fecha de fin: si no se especifica, se toma la fecha timestamp de ahora.
    analizador.add_argument(
        '-f',
        metavar='final',
        help="Fecha final del rango de fechas en formato 'DD-MM-AAAA' (por defecto, hoy)."
    )

    # Extraer los argumentos.
    analizador = analizador.parse_args()

    # Devolver los argumentos de entrada.
    return analizador.i, analizador.f


def tratar_fechas(inicio, final):
    """
    Corrige las fechas introducidas verificando que están
    correctamente ordenadas o que el formato es correcto.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Fechas parseadas para la ejecución del programa.
    """

    try:
        # Comprobar los argumentos recibidos.
        if inicio and not final:
            """
            No se indicó la fecha final, así que se interpreta como la fecha actual.
            """

            inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
            final = datetime.datetime.now()

        elif not inicio and final:
            """
            No se indicó la fecha inicial, así que se interpreta como la fecha 0 (01-01-1970).
            """

            inicio = datetime.datetime.fromtimestamp(0)
            final = datetime.datetime.strptime(final, '%d-%m-%Y')

        elif not inicio and not final:
            """
            No se indicó ninguna fecha, así que se interpretan 'desde hace un mes hasta hoy'.
            'Un mes' es mi elección como rango por defecto.
            """

            # Fecha de ejecución del programa.
            ahora = datetime.datetime.now()

            # Un mes antes de la fecha de hoy.
            inicio = ahora - datetime.timedelta(days=30)
            final = ahora

            print('No se indicaron fechas. Se usará rango por defecto: 30 días atrás.\n')

        elif inicio == final:
            """
            Se indicaron las mismas fechas, así que se interpretan como 'todo el día de hoy'.
            """

            inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
            final = inicio + datetime.timedelta(days=1)

        else:
            """
            Se indicaron las fechas correctamente.
            """

            inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
            final = datetime.datetime.strptime(final, '%d-%m-%Y')

            # Comprobar que las fechas están ordenadas.
            if final < inicio:
                print("La fecha inicial es posterior a la fecha final, ¿invertir fechas y ejecutar? [s/n]")

                # Leer la respuesta del usuario.
                respuesta = input().lower()

                # Preguntar si se quiere invertir las fechas.
                if respuesta == 's':
                    inicio, final = final, inicio

                    print("Fechas invertidas.")

                else:
                    # Humor.
                    if respuesta == 'n':
                        print("Has intentado desafiar las leyes del espacio-tiempo.")

                    else:
                        print("Opción no válida.")

                    exit()

    except:
        print("Formato de fecha no válido: asegúrate de usar el formato 'DD-MM-AAAA'.")
        exit()

    return inicio, final


def ficheros(ruta, extension):
    """
    Lista los ficheros de una ruta, incluidos subdirectorios.

    :param ruta: Ruta del directorio.
    :param extension: Extensión de los ficheros a listar.

    :return: Lista de ficheros.
    """

    # Lista de ficheros.
    lista = []

    # Listar los ficheros de la ruta.
    for ruta, _, ficheros in os.walk(ruta):

        # Comprobar que el fichero tiene la extensión indicada.
        for fichero in ficheros:
            if extension is None or fichero.endswith("." + extension):
                lista.append(os.path.join(ruta, fichero))       # Añadir el fichero a la lista.

    return lista


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def cambios_ramas_registro():
    """
    Obtiene los cambios de ramas registrados en el registro del sistema en un intervalo de fechas.

    :return: lista de fechas en las que se cambiaron el registro.
    """

    # Conjunto de fechas en las que se cambiaron ramas del registro.
    fechas = set()

    # Tipos de registros a analizar
    tipos_clave = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

    # Obtener los cambios de ramas registrados.
    for clave in tipos_clave:
        # Obtener el manjeador de registros.
        manejador = winreg.OpenKey(clave, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")

        # Obtener el timestamp de la última actualización.
        timestamp = winreg.QueryInfoKey(manejador)[2] / 10000000 - 11644473600

        # Obtener la fecha del cambio (en formato 'DD-MM-AAAA').
        fecha = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y')

        # Añadir la fecha al conjunto.
        fechas.add(fecha)

    return fechas


def archivos_recientes(inicio, final):
    """
    Obtiene los archivos recientes en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de archivos recientes.
    """

    # Conjunto de archivos recientes
    archivos = set()

    # Obtener el directorio de archivos reciente por defecto.
    directorio = os.environ['USERPROFILE'] + '\\AppData\\Roaming\\Microsoft\\Windows\\Recent'

    # Obtener todos enlaces directos del directorio de archivos recientes.
    for archivo in os.listdir(directorio):
        # Comprobar que el elemento es un archivo '.lnk' (enlace simbólico de Windows).
        if archivo.endswith('.lnk'):
            # Obtener la ruta real de los enlaces.
            shell = win32com.client.Dispatch("WScript.Shell")
            ruta = shell.CreateShortCut(directorio + '\\' + archivo).targetpath

            if os.path.isfile(ruta):
                # Obtener la fecha de creación del enlace (sin la hora).
                fecha = datetime.datetime.fromtimestamp(os.path.getctime(directorio + '\\' + archivo))

                # Comprobar que el archivo está dentro del rango de fechas.
                if inicio <= fecha <= final:
                    archivos.add(ruta)

    return archivos


def archivos_temporales(inicio, final):
    """
    Obtiene los archivos temporales en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de archivos temporales.
    """

    # Conjunto de archivos temporales
    archivos = set()

    # Obtener el directorio de archivos temporales por defecto.
    directorio = os.environ['USERPROFILE'] + '\\AppData\\Local\\Temp'

    # Obtener todos enlaces directos del directorio de archivos temporales.
    for archivo in ficheros(directorio, None):
        try:
            # Obtener la fecha de creación del archivo.
            fecha = datetime.datetime.fromtimestamp(os.path.getctime(archivo))

            # Comprobar que el archivo está dentro del rango de fechas.
            if inicio <= fecha <= final:
                archivos.add(archivo)

        except:
            pass

    return archivos


def programas_abiertos():
    """
    Obtiene los procesos abiertos en este momento.
    Los "programas" abiertos según el subject en español.

    :return: Lista de procesos abiertos.
    """

    # Lista de procesos abiertos.
    procesos = []

    # Obtener todos los procesos abiertos.
    for proceso in conexion.Win32_Process():
        procesos.append(proceso.Name)

    return procesos


def programas_instalados(inicio, final):
    """
    Obtiene los programas instalados en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de programas instalados.
    """

    # TODO: revisar, ¿se puede considerar un '.exe' como un programa?

    # Conjunto de programas instalados.
    programas = set()

    # Listar todos los ficheros ejecutables del sistema.
    for fichero in ficheros('C:\\', 'exe'):
        try:
            fecha = datetime.datetime.fromtimestamp(os.path.getctime(fichero))      # Obtener la fecha de creación.

            # Comprobar que el fichero se creó en el rango de fechas.
            if inicio <= fecha <= final:
                programas.add(fichero)      # Añadir el fichero al conjunto

        except:
            pass

    return programas


def historial_navegacion(inicio, final):
    """
    Obtiene el historial de navegación en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de historial de navegación.
    """

    # Desactivar mensajes de logging para evitar 'INFO: <browser> ...'.
    logging.disable(logging.CRITICAL)

    # Conjunto de entradas de todos los historiales.
    entradas = set()

    # Entradas de los historiales de todos los navegadores instalados.
    historiales = get_history().histories

    for entrada in historiales:
        # Obtener datos de la tuplpa.
        fecha, url = entrada

        # Tratar fecha (ya que se obtiene con zona horaria)
        fecha = fecha.replace(tzinfo=None)

        # Comprobar que la entrada está dentro del rango de fechas.
        if inicio <= fecha <= final:
            entradas.add(url)

    return entradas


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos.
    inicio, final = leer_argumentos()

    # Tratar las fechas recibidas.
    inicio, final = tratar_fechas(inicio, final)

    # Establecer conexión con el sistema.
    conexion = wmi.WMI()

    # Obtener los cambios en las ramas de registro.
    cambios = cambios_ramas_registro()

    # Imprimir los cambios en las ramas de registro.
    print("Cambios en las ramas de registro:")

    for cambio in cambios:
        print("\t" + cambio)

    # Obtener los archivos recientes en un rango de fechas.
    recientes = archivos_recientes(inicio, final)

    # Imprimir los archivos recientes.
    print("Archivos recientes:")

    for reciente in recientes:
        print("\t" + reciente)

    # Obtener los archivos temporales en un rango de fechas.
    temporales = archivos_temporales(inicio, final)

    # Imprimir los archivos temporales.
    print("Archivos temporales:")

    for temporal in temporales:
        print("\t" + temporal)

    # Obtener los programas abiertos en un rango de fechas.
    abiertos = programas_abiertos()

    # Imprimir los programas abiertos.
    print("Programas (procesos) abiertos:")

    for programa in abiertos:
        print("\t" + programa)

    # Obtener programas instalados en un rango de fechas.
    instalados = programas_instalados(inicio, final)

    # Imprimir los programas instalados.
    print("Programas instalados:")

    for programa in sorted(instalados):
        print("\t" + programa)

    # Obtener el historial de navegación en un rango de fechas.
    historial = historial_navegacion(inicio, final)

    # Imprimir el historial de navegación.
    print("Historial de navegación:")

    for entrada in historial:
        print("\t" + entrada)

    # Obtener el directorio actual.
    # directorio_actual = os.getcwd()

    # Obtener el nombre del fichero.
    # fichero = os.path.basename(__file__)

    # Obtener la ruta del fichero.
    # ruta = os.path.join(directorio_actual, fichero)
