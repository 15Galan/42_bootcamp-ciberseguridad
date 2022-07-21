import requests
import bs4

# PROBLEMA:
# Crear un programa con una función llamada 'spider' que extraiga todas las imágenes de un sitio
# web recursivamente, proporcionando una URL como parámetro y que gestione las siguientes opciones:
# '-r': descarga de forma recursiva las imágenes de una URL.
# '-r -l [n]': la acción de '-r', pero hasta 'n' niveles de profundidad.
# '-p [path]': indica la ruta donde se guardarán los archivos descargados (si no se indica, se usará './data/').

# ----------------------------------------------------------------------------------------------------------------------

# Variables Globales (y sus valores por defecto).
sitios_encontrados = set()      # Conjunto de URLs de sitios, sin repetir
imagenes_encontradas = set()    # Conjunto de URLs de imágenes, sin repetir


# TODO: renombrar a 'spider'
# Extrae todas las URLs de otros sitios web, de un sitio web.
# - URL:    URL del sitio web del que extraer los otros sitios web.
def obtener_sitios(sitio_web):
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
def obtener_imagenes(sitios_web):
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
    # TODO: pedir datos al usuario
    url = "https://google.com"
    nivel = 0

    sitios_encontrados.add(url)  # Añadir el sitio inicial

    print("URL inicial: " + url)
    print("Nivel (dft): " + str(nivel))

    obtener_sitios(url)

    print("\nSitios encontrados:")
    for url in sorted(sitios_encontrados):
        print(url)

    obtener_imagenes(sitios_encontrados)

    print("\nImágenes encontradas:")
    for url in sorted(imagenes_encontradas):
        print(url)
