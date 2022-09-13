# Introducción

Este proyecto introduce conceptos específicos sobre la fortaleza del **algoritmo RSA** y sus vulnerabilidades potenciales.
Si bien el algoritmo es considerado suficientemente fuerte para la potencia computacional de los dispositivos actuales,
**ciertas formas de utilizarlo pueden llevar a graves problemas de seguridad**.

Concretamente, este proyecto trata sobre un [ataque de Wiener](https://en.wikipedia.org/wiki/Wiener%27s_attack) que
permite recuperar la clave privada de un par de claves RSA a partir de la clave pública.


# Objetivo

Crear una herramienta escrita en C que permita:
- [x] Extraer la clave pública de 2 certificados y obtenga tanto el módulo como el exponente de cada una de ellas.
- [x] Reconstruir la clave privada a partir de 2 primos y su producto.
- [x] Reconstruir la clave simétrica cifrada con él.


# Funcionamiento

## Generar claves archivos de prueba

La carpeta _Recursos_ contiene un script de Python que permite generar certificados y claves RSA que cumplen con las
circunstancias descritas (ambos certificados tienen un mismo número primo en común), además de un fichero de texto
cifrado con la clave simétrica cuyo contenido se debe recuperar teniendo éxito en la implementación del programa.

## Compilar y ejecutar la herramienta `coRSAir`

Para compilar y ejecutar el programa:

```bash
make
```
- Las rutas indicadas en el fichero _Makefile_ son absolutas, ya que se ejecutaba en un equipo del campus.
- El archivo _Makefile_ indica que se tomarán como argumentos los certificados en la carpeta _Recursos_.
