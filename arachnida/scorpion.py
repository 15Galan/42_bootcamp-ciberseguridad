import argparse

from PIL import Image
from PIL.ExifTags import TAGS


# PROBLEMA:
# Crear un programa con una función llamada 'scorpion' que
# extraiga metadatos de las imágenes que reciba como argumento.
# '-r': descarga de forma recursiva las imágenes de una URL.
# '-l [n]': la acción de '-r', pero hasta 'n' niveles de profundidad.
# '-p [path]': indica la ruta donde se guardarán los archivos descargados (si no se indica, se usará './data/').


# ----------------------------------------------------------------------------------------------------------------------


def inicializar_analizador():
    parser = argparse.ArgumentParser(
        # prog = "./scorpion",
        description="Muestra los metadatos de imágenes."
    )

    parser.add_argument("IMAGEN", help="Imagen a analizar", type=str)
    parser.add_argument("IMAGENES", help="Imágenes a analizar.", nargs="*")
    parser.add_argument("-r", help="remove the metadata shown from the image(s)", action="store_true", default=False)

    return parser.parse_args()


if __name__ == "__main__":
    args = inicializar_analizador()

    eliminar = args.r

    ubicaciones = list()
    ubicaciones.append(args.IMAGEN)
    ubicaciones += args.IMAGENES

    for ubicacion in ubicaciones:
        try:
            imagen = Image.open(ubicacion)

        except:
            print(f"Couldnt open {ubicacion}")

        else:
            print(f"{'Nombre':32}: {imagen.filename}")
            print(f"{'Dimensiones':32}: {imagen.size[0]}, {imagen.size[1]}")

            datos = imagen.getexif()

            for id in datos:
                try:
                    nombre = TAGS.get(id)
                    valor = datos.get(id)

                    print(f"{nombre:25}: {valor}")

                except Exception:
                    print(f"Etiqueta {id} no encontrada.")

            if (eliminar):
                imagen.save(ubicacion)

        print("-" * 80)
