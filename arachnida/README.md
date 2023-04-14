# Introducción

Los **metadatos** son información que se utiliza para describir otros datos; esencialmente, son **datos sobre datos**.

Se utilizan frecuentemente en imágenes y documentos, **pudiendo llegar a revelar información sensible** de quienes lo han creado o manipulado.


# Objetivo

Crear 2 instrumentos ($\texttt{spider}$ y $\texttt{scorpion}$) que permitan extraer información de una web automáticamente y después analizarla para conocer o eliminar datos sensibles; ambos programas pueden ser scripts o binarios.

Pueden usarse funciones o librerías que permitan crear peticiones HTTP y manejar archivos, pero la lógica de cada programa debe estar desarrollada por mí; es decir, no pueden utilizarse $\texttt{wget}$, $\texttt{scrapy}$, ni librerías similares.


# Funcionamiento

## spider

Este programa debe recibir como argumento una URL de la que extraerá las imágenes.

```console
$ python3 spider.py -h

usage: spider.py [-h] [-r] [-l L] [-p P] [-v] [-e] [-o] URL

Herramienta casera de Scraping de imágenes de un sitio web.

positional arguments:
  URL         URL del sitio web a 'scrapear'

optional arguments:
  -h, --help  show this help message and exit
  -r          Indica que la búsqueda y descarga de imágenes será recursiva (por defecto L=5).
  -l L        Nivel de profundidad para la búsqueda y descarga de imágenes.
  -p P        Ruta de la carpeta donde descargar las imágenes.
  -v          Muestra las URLs visitadas durante la ejecución.
  -e          Muestra las URLs fallidas y su error durante la ejecución.
  -o          Muestra las URLs visitadas ordenadas alfabéticamente al terminar.

Ejercicio 'arachnida' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).
```


## scorpion

Este programa debe recibir como argumento una o varias imágenes de las que extraerá sus metadatos.

> [!NOTE]
> Normalmente, las imágenes publicadas en Internet carecen de metadatos por seguridad.

```console
$ python3 scorpion.py -h

usage: scorpion.py [-h] IMAGEN [IMAGENES [IMAGENES ...]]

Herramienta casera que muestra metadatos de imágenes.

positional arguments:
  IMAGEN      Imagen a analizar
  IMAGENES    Imágenes a analizar.

optional arguments:
  -h, --help  show this help message and exit

Ejercicio 'arachnida' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).
```
