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
import wmi
import os


# ----------------------------------------------------------------------------------------------------------------------


def leer_argumentos():
    """
    Lee los argumentos de entrada de la línea de comandos.

    :return: Valor y opciones de los argumentos leídos.
    """

    # Leer los argumentos de entrada.
    analizador = inicializar_analizador()

    # Devolver los argumentos de entrada.
    return analizador.i, analizador.f


def inicializar_analizador():
    """
    Inicializa el analizador de argumentos.

    :return: Objeto del analizador de argumentos.
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

    # Devolver el analizador de argumentos.
    return analizador.parse_args()


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
            No se indicó la fecha inicial, así que se interpreta como la fecha 0 (01-01-2970).
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
        print("Formato de fecha no válido.")
        exit()

    return inicio, final


def actividad_usuario(inicio, final):
    """
    Obtiene la actividad del usuario en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de actividad del usuario.
    """

    # TODO: implementar

    return None


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


def programas_abiertos(inicio, final):
    """
    Obtiene los programas abiertos en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de programas abiertos.
    """

    # TODO: implementar

    return None


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
            if fichero.endswith("." + extension):
                lista.append(os.path.join(ruta, fichero))       # Añadir el fichero a la lista.

    return lista


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
        fecha = datetime.datetime.fromtimestamp(os.path.getctime(fichero))      # Obtener la fecha de creación.

        # Comprobar que el fichero se creó en el rango de fechas.
        if inicio <= fecha <= final:
            programas.add(fichero)      # Añadir el fichero al conjunto

    return programas


def historial_navegacion(inicio, final):
    """
    Obtiene el historial de navegación en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de historial de navegación.
    """

    # TODO: implementar

    return None


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos.
    inicio, final = leer_argumentos()

    # Tratar las fechas recibidas.
    inicio, final = tratar_fechas(inicio, final)

    # Establecer conexión con el sistema.
    conexion = wmi.WMI()

    # Obtener la actividad del usuario en un rango de fechas.
    # actividades = actividad_usuario(inicio, final)

    # Imprimir la actividad del usuario.
    # print("Actividad del usuario:")

    # for actividad in actividades:
    #     print("\t" + actividad)

    # Obtener los archivos recientes en un rango de fechas.
    recientes = archivos_recientes(inicio, final)

    # Imprimir los archivos recientes.
    print("Archivos recientes:")

    for reciente in recientes:
        print("\t" + reciente)

    # Obtener programas instalados en un rango de fechas.
    instalados = programas_instalados(inicio, final)

    # Imprimir los programas instalados.
    print("Programas instalados:")

    for programa in sorted(instalados):
        print("\t" + programa)

    # Obtener los programas abiertos en un rango de fechas.
    # abiertos = programas_abiertos(inicio, final)

    # Imprimir los programas abiertos.
    # print("Programas abiertos:")

    # for programa in abiertos:
    #     print("\t" + programa)

    # Obtener el historial de navegación en un rango de fechas.
    # historial = historial_navegacion(inicio, final)

    # Imprimir el historial de navegación.
    # print("Historial de navegación:")

    # for entrada in historial:
    #     print("\t" + entrada)

    # Obtener el directorio actual.
    # directorio_actual = os.getcwd()

    # Obtener el nombre del fichero.
    # fichero = os.path.basename(__file__)

    # Obtener la ruta del fichero.
    # ruta = os.path.join(directorio_actual, fichero)
