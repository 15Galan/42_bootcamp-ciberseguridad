# Stockholm
## Descripción
Programa "ransomware" que cifra los ficheros de la carpeta `home/usuario/infection` y/o los descifra, dentro de dicha carpeta o en otra distina.

## Prerrequisitos
- Un entorno Python y con los módulos `argparse`, `os`, `Fernet` y `pathlib`.
- Una carpeta `/home/usuario/infection` con ficheros.

Al tratarse de un script, **no es necesario compilarlo**.

## Características
- Solo busca ficheros a cifrar en la carpeta `/home/usuario/infection`.
- Las extensiones a cifrar serán las mismas [extensiones](https://gist.github.com/xpn/facb5692980c14df272b16a4ee6a29d5) que cifró WannaCry.
- Los ficheros descifrados se mantendrán en la carpeta original o se moverán a una especificada (solo los descifrados).
- Tras cifrar los archivos, la clave de cifrado se almacena en `clave.key`, en la ruta de `stockholm.py`, para usarla con la opción `-r` al descifrar.

## Manual de usuario
### Funcionamiento
```
usage: stockholm.py [-h] [-r clave] [-v] [-s] [-p carpeta]

Herramienta casera para 'secuestrar' y 'liberar' ficheros.

optional arguments:
  -h, --help  show this help message and exit
  -r clave    revierte la infección usando la clave de cifrado.
  -v          versión del programa.
  -s          desactiva la información mostrada por pantalla.
  -p carpeta  descifra todos los ficheros y los almacena en la carpeta indicada.

Ejercicio 'stockholm' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).
```

### Ejemplos básicos
Cifrar todos los archivos de `home/usuario/infection`.
```shell
$ python3 stockholm.py
```

Descifrar los archivos de `/home/usuario/infection` en la misma carpeta.
```
$ python3 stockholm.py -r clave.key
```

Descifrar los archivos de `/home/usuario/infection` en la ruta indicada.
```
$ python3 stockholm.py -r clave.key -p /home/srgalan/desinfection
```

