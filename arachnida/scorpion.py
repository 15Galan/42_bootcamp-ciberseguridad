import argparse

from PIL import Image
from PIL.ExifTags import TAGS


# PROBLEMA:
# Crear un programa con una función llamada 'scorpion' que
# extraiga metadatos de las imágenes que reciba como argumento.
# Debe ser compatible con las extensiones de los archivos que
# maneje el script 'spider'.

# ----------------------------------------------------------------------------------------------------------------------


# Inicializa el parser de argumentos de la línea de comandos.
def inicializar_analizador():
    # Analizador de los argumentos de la línea de comandos
    parser = argparse.ArgumentParser(
        # prog = "./scorpion",
        description="Herramienta casera que muestra metadatos de imágenes.",
        epilog="Ejercicio 'arachnida' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga)."
    )

    # Agregar las opciones de la línea de comandos
    parser.add_argument("IMAGEN", help="Imagen a analizar", type=str)
    parser.add_argument("IMAGENES", help="Imágenes a analizar.", nargs="*")

    # Obtener los argumentos de la línea de comandos
    return parser.parse_args()


# Extrae los metadatos de
def scorpion(rutas):
    for ruta in rutas:
        try:
            # Abrir la imagen
            imagen = Image.open(ruta)

        except:
            print(f"No se pudo abrir {ruta}.")

        else:
            # Mostrar los metadatos básicos de la imagen
            print(f"{'Nombre':32}: {imagen.filename.split('/')[-1]}")           # Solo el nombre, no la ruta
            print(f"{'Dimensiones':32}: {imagen.size[0]}, {imagen.size[1]}")
            print(f"{'Formato':32}: {imagen.format}")
            print(f"{'Modo':32}: {imagen.mode}")
            print(f"{'Paleta':32}: {imagen.palette}")

            # Indicar si no tiene datos EXIF
            if not imagen.getexif():
                print(f"{'Exif':32}: {imagen.getexif()}")

            print()

            # Extraer los metadatos EXIF
            datos = imagen.getexif()

            # Mostrar los metadatos EXIF como "Nombre : Valor"
            for id in datos:
                try:
                    nombre = TAGS.get(id)
                    valor = datos.get(id)

                    print(f"{nombre:32}: {valor}")

                except Exception:
                    print(f"Etiqueta {id} no encontrada.")

        print("-" * 80)


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    args = inicializar_analizador()

    # Leer las imágenes desde la línea de comandos
    ubicaciones = list()
    ubicaciones.append(args.IMAGEN)
    ubicaciones += args.IMAGENES

    scorpion(ubicaciones)
