import argparse
import requests
import os

from bs4 import BeautifulSoup as sopa
from urllib.parse import urlparse


# PROBLEMA:
# Crear un programa con una función llamada 'spider' que extraiga todas las imágenes de un sitio
# web recursivamente, proporcionando una URL como parámetro y que gestione las siguientes opciones:
# '-r': descarga de forma recursiva las imágenes de una URL.
# '-l [n]': la acción de '-r', pero hasta 'n' niveles de profundidad.
# '-p [path]': indica la ruta donde se guardarán los archivos descargados (si no se indica, se usará './data/').


# ----------------------------------------------------------------------------------------------------------------------


# Variables Globales (y sus valores por defecto).
sitios_encontrados = set()      # Conjunto de URLs de sitios, sin repetir
imagenes_encontradas = set()    # Conjunto de URLs de imágenes, sin repetir


# Inicializa el parser de argumentos de la línea de comandos.
def inicializar_analizador():
    # Analizador de los argumentos de la línea de comandos
    analizador = argparse.ArgumentParser(
        # prog="./spider",
        description="Herramienta casera de Scraping de imágenes de un sitio web.",
        epilog="Ejercicio 'arachnida' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga)."
    )

    # Agregar las opciones de la línea de comandos
    analizador.add_argument("URL", help="URL del sitio web a 'scrapear'", type=str)
    analizador.add_argument("-r", help="Indica que la búsqueda y descarga de imágenes será recursiva (por defecto L=5).", action="store_true")
    analizador.add_argument("-l", help="Nivel de profundidad para la búsqueda y descarga de imágenes", type=int, default=5)
    analizador.add_argument("-p", help="Ruta de la carpeta donde descargar las imágenes", type=str, default="./data/")
    analizador.add_argument("-v", help="Muestra las URLs visitadas durante la ejecución", action="store_true")
    analizador.add_argument("-e", help="Muestra las URLs fallidas y su error durante la ejecución", action="store_true")
    analizador.add_argument("-o", help="Muestra las URLs visitadas ordenadas alfabéticamente al terminar", action="store_true")

    # Obtener los argumentos de la línea de comandos
    return analizador.parse_args()


# Extrae todas las URLs de otros sitios web, de un sitio web.
# - URL:    URL del sitio web del que extraer los otros sitios web.
# - niv:    Nivel de profundidad actual de la búsqueda.
def extraer_sitios(sitio_web, niv):
    try:
        # Obtener el contenido de la URL
        respuesta = requests.get(sitio_web, timeout=5)

        # Código 200: petición exitosa
        if respuesta.status_code == 200:
            # Convertir el contenido a un objeto XML
            xml = sopa(respuesta.content, "html.parser")

            # Obtener todos los elementos <a> del XML (URLs)
            enlaces = xml.find_all("a")

            # Recorremos todos los elementos <a>
            for enlace in enlaces:
                # Obtener la URL del sitio
                esquema, dominio, ruta = formatear(sitio_web, enlace.get("href"))
                url = esquema + "://" + dominio + ruta

                # Añadir el sitio si no está repetido
                if url not in sitios_encontrados:
                    sitios_encontrados.add(url)

                    # Mostrar el sitio web encontrado
                    if verbose:
                        print("   " * niv, url)     # Se usan espacios para indentar

                    # Recursividad: extraer los otros sitios web
                    # si aún no se alcanzó la profundidad indicada
                    if niv < nivel:
                        extraer_sitios(url, niv + 1)

    except Exception as excepcion:
        if errores:
            print(niv, excepcion.args)


# Extrae todas las imágenes de un sitio web como URLs.
def extraer_imagenes(sitios_web):
    for sitio in sitios_web:
        try:
            # Obtener el contenido de la URL
            respuesta = requests.get(sitio, timeout=5)

            # Convertir el contenido a un objeto XML
            xml = sopa(respuesta.content, "html.parser")

            # Obtener todos los elementos <img> del XML
            enlaces = xml.find_all("img")

            # Recorrer todos los elementos <img>
            for enlace in enlaces:
                # Obtener la URL de la imagen
                esquema, dominio, ruta = formatear(sitio, enlace.get("src"))
                url = esquema + "://" + dominio + ruta

                # Añadir la imagen si no está repetida
                if url not in imagenes_encontradas and compatible(url):
                    imagenes_encontradas.add(url)

                    # Mostrar la imagen encontrada
                    if verbose:
                        print(url)

        except Exception as excepcion:
            if errores:
                print(excepcion.args)


# Indica si una URL corresponde a un archivo de algún tipo disponible.
def compatible(url):
    extensiones = ["jpg", "jpeg", "png", "gif", "bmp", "docx", "pdf"]

    # Comprobar si el final de la URL recibida (extensión del
    # archivo) coincide con alguno de los formatos disponibles
    for extension in extensiones:
        if url.endswith(extension):
            return True

    return False


# Recibe una URL visitada y una URL a visitar, corrigiendo esta última
# si está mal formada, usando o no los datos de la URL visitada.
def formatear(anterior, siguiente):
    anterior = urlparse(anterior)   # Actualizar la variable (URL anterior en componentes)
    siguiente = urlparse(siguiente) # Actualizar la variable (URL siguiente en componentes)

    # Componentes de la URL siguiente
    esquema, dominio, ruta, fragmento = siguiente.scheme, siguiente.netloc, siguiente.path, siguiente.fragment

    # Si la URL siguiente no tiene esquema, se le asigna el mismo que la URL anterior (es una subpágina)
    if esquema == "":
        esquema = anterior.scheme

    # Si la URL siguiente no tiene dominio, se le asigna el mismo que la URL anterior (es una subpágina)
    if dominio == "":
        dominio = anterior.netloc

    # Si la URL siguiente no tiene "www.", se le añade (puramente estético)
    elif not dominio.startswith("www."):
        dominio = "www." + dominio

    # Si la URL siguiente no tiene ruta, se le asigna la misma que la URL anterior (es una subpágina)
    if ruta == "" or ruta == "/":
        ruta = anterior.path

    # Si la URL siguiente tiene un fragmento, las URL anterior y siguiente son la misma
    if fragmento != "":
        ruta = ""

    return esquema, dominio, ruta


# Descarga las imágenes recibidas como parámetro en la
# carpeta indicada en los argumentos de la línea de comandos.
def descargar_imagenes(imagenes, carpeta):
    for imagen in imagenes:
        try:
            # Obtener el contenido de la URL
            respuesta = requests.get(imagen, timeout=5)

            # Código 200: petición exitosa
            if respuesta.status_code == 200:
                # Obtener el nombre del archivo
                nombre = imagen.split("/")[-1]

                # Crear la carpeta si no existe
                if not os.path.exists(carpeta):
                    os.makedirs(carpeta)

                # Guardar el archivo en la carpeta indicada
                with open(carpeta + "/" + nombre, "wb") as archivo:
                    archivo.write(respuesta.content)

        except Exception as excepcion:
            if errores:
                print(excepcion.args)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    global url, nivel, carpeta, verbose, errores, orden

    # Inicializar el analizador de la línea de comandos
    args = inicializar_analizador()

    # Obtener los argumentos del comando
    url = args.URL
    nivel = args.l
    carpeta = args.p
    rec = args.r
    verbose = args.v
    errores = args.e
    orden = args.o


    # Extraer todas las URLs necesarias
    print("Analizando las páginas...")

    if rec:
        extraer_sitios(url, 0)          # Extraer todos los sitios web

    else:
        sitios_encontrados.add(url)     # Añadir solamente la URL inicial


    # Extraer las imágenes de las URLs anteriores
    print("Extrayendo imágenes...")
    extraer_imagenes(sitios_encontrados)

    # Descargar las imágenes anteriores
    print("Descargando imágenes...")
    descargar_imagenes(imagenes_encontradas, carpeta)

    # Mostrar las consultas ordenadas alfabéticamente
    if orden:
        print("Resumen de la búsqueda:")

        for sitio in sorted(sitios_encontrados):
            print(sitio)

        print("\nResumen de las imágenes:")

        for imagen in sorted(imagenes_encontradas):
            print(imagen)
