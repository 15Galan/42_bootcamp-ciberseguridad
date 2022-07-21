import argparse
import requests
import bs4



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
    analizador.add_argument("-p", help="Ruta de la carpeta donde descargar las imágenes", type=str)
    analizador.add_argument("-v", help="Muestra las URLs visitadas durante la ejecución", action="store_true")
    analizador.add_argument("-e", help="Muestra las URLs fallidas y su error durante la ejecución", action="store_true")
    analizador.add_argument("-o", help="Muestra las URLs visitadas ordenadas alfabéticamente al terminar", action="store_true")

    # Obtener los argumentos de la línea de comandos
    return analizador.parse_args()

    return argumentos

# TODO: renombrar a 'spider'
# Extrae todas las URLs de otros sitios web, de un sitio web.
# - URL:    URL del sitio web del que extraer los otros sitios web.
def extraer_sitios(sitio_web):
    # Obtener el contenido de la URL
    respuesta = requests.get(sitio_web)

    # Convertir el contenido a un objeto XML
    xml = bs4.BeautifulSoup(respuesta.content, "html.parser")

    # Obtener todos los elementos <a> del XML
    enlaces = xml.find_all("a")

    # Recorremos todos los elementos <a>
    for enlace in enlaces:
        # Obtener la URL del sitio
        url = enlace.get("href")

        # Añadir el sitio si no está repetido
        if url not in sitios_encontrados:
            sitios_encontrados.add(url)


# Extrae todas las imágenes de un sitio web como URLs.
def extraer_imagenes(sitios_web):
    # Solo si hay algún sitio web almacenado
    if sitios_web:
        for sitio in sitios_web:
            # Obtener el contenido de la URL
            respuesta = requests.get(sitio)

            # Convertir el contenido a un objeto XML
            xml = bs4.BeautifulSoup(respuesta.content, "html.parser")

            # Obtener todos los elementos <img> del XML
            url_imagenes = xml.find_all("img")

            # Recorrer todos los elementos <img>
            for url in url_imagenes:
                # Obtener la URL de la imagen
                imagen = url.get("src")

                # Añadir la imagen si no está repetida
                if imagen not in imagenes_encontradas and compatible(imagen):
                    imagenes_encontradas.add(imagen)


# Indica si una URL corresponde a un archivo de algún tipo disponible.
def compatible(url):
    extensiones = ["jpg", "jpeg", "png", "bmp"]

    # Comprobar si el final de la URL recibida (extensión del
    # archivo) coincide con alguno de los formatos disponibles
    for extension in extensiones:
        if url.endswith(extension):
            return True

    return False


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    global url, nivel, carpeta, verbose, errores, orden

    # Inicializar el analizador de la línea de comandos
    args = inicializar_analizador()

    # Obtener los argumentos del comando
    url = args.URL
    rec = args.r
    nivel = args.l
    verbose = args.v
    errores = args.e
    orden = args.o

    # Si se indica la carpeta, se usa;
    # si no, se usa la ruta por defecto
    if args.p:
        carpeta = args.p

    else:
        carpeta = "./data/"

    # Extraer todas las URLs necesarias
    print("Analizando las páginas...")
    extraer_sitios(url, 0)

    if orden:
        print("Resumen de la búsqueda:")
        for sitio in sorted(sitios_encontrados):
            print(sitio)

    print("\nImágenes encontradas:")
    for url in sorted(imagenes_encontradas):
        print(url)
