# Objetivo

Implementar un sistema TOTP (*Time-Based One Time Password*) en cualquier lenguaje, que sea capaz de generar contraseñas
efímeras a partir de una **clave maestra**.

- Estará basado en el **[RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238)**.
- Puede comprobarse que el programa funciona correctamente con la herramienta `oathtool`.

```bash
$ oathtool -totp $(cat key.hex)
```


## Requisitos

El programa debe poder registrar una clave inicial y ser capaz de generar una contraseña nueva cada vez que se solicite.

Puede utilizarse cualquier librería que no sea TOTP (es decir, que no haga el trabajo sucio).

- [x] El programa debe llamarse `ft_otp`.
- [x] Opción `-g`: el programa recibe como argumento una clave hexadecimal de al menos 64 caracteres.
	- [x] El programa guardará dicha clave en un fichero `ft_otp.key`, siempre cifrado.
- [x] Opción  `-k`: el programa generará una nueva contraseña temporal y la mostrará en la salida estándar.


## Ejemplo de uso

```bash
$ echo -n "Hola Mundo" > key.txt
$ ./ft_otp -g ket.txt

Error: la clave debe ser de al menos 64 caracteres hexadecimales.

$ xxd -p key.txt > key.hex
$ cat key.hex | wc -c
$ ./ft_otp -g key.hex

Clave almacenada en 'ft_otp.key'

$ ./ft_otp -k ft_otp.key

Se generó la clave '836492'

$ sleep 60
$ ./ft_otp -k ft_otp.key

Se generó la clave '123518'
```

> Recomiendo usar `xxd -p -c 256 key.txt > key.hex` para evitar saltos de línea.
> 
> ---
> 
> Esto aumentará el número de columnas de la representación al máximo, evitando que el programa coloque `\n` no deseados cada cierto número de columnas.
> Por defecto, se interpreta `-c 16`.


# Funcionamiento

Para usar el programa, primero será necesario replicar los pasos del [ejemplo](#ejemplo-de-uso) para generar una clave
hexadecimal de al menos 64 caracteres; la clave maestra.

Una vez se tenga un fichero con la clave, el programa puede usarse:

```bash
python3 ft_otp.py -h
```
```
usage: ft_otp.py [-h] [-g fichero] [-k fichero] [-qr fichero]

Herramienta casera para generar contraseñas TOTP.

optional arguments:
  -h, --help   show this help message and exit
  -g fichero   almacena una clave hexadecimal de 64 caracteres mínimo en un
               fichero 'ft_otp.key'.
  -k fichero   genera una contraseña temporal usando un fichero y la muestra
               por pantalla.
  -qr fichero  muestra un QR con la clave secreta.

Ejercicio 'ft_otp' del Bootcamp de Ciberseguridad de la Fundación 42 (Málaga).
```

## Generar una clave

```bash
python3 ft_otp.py -g key.hex
```

Este fichero cifrado se puede usar para generar contraseñas temporales.


## Generar una contraseña

Usando el fichero obtenido en el apartado anterior:

```bash
python3 ft_otp.py -k ft_otp.key
```

Esto genera un código de 6 dígitos que se puede usar para iniciar sesión en cualquier servicio que use TOTP.

> **Nota**: el código generado es válido durante 30 segundos, por lo que es necesario esperar 30 segundos para obtener un nuevo código.


## Mostrar un QR

```bash
python3 ft_otp.py -qr ft_otp.key
```

Esto muestra un código QR con la clave secreta.

> **Nota**: si bien el código QR solo muestra la clave compartida, lo normal es que muestre una URL del servicio de
> autenticación con los datos necesarios, que es lo que permite que su lectura sea automática.
> Sin embargo, como el proyecto especificaba mostrar _la clave compartida_, me he limitado a implementar lo pedido.
