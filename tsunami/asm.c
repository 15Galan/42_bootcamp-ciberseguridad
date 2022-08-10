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

        sub  esp, 0Ch                   ; 0x0C = 12, porque se usan 10 lineas (pero mul.4)

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

        lea eax, [ebp-0Bh]              ; Ultima posicion de 'msvcrt.dll' (ebp - 08h)

        push eax
        mov ebx, 0x7c801d7b             ; Direccion de la libreria 'LoadLibrary'
        call ebx


        ; Cargar la Calculadora ('calc.exe')
        ; system(calc.exe)

        push ebp
        mov  ebp, esp
        xor  edi, edi
        push edi

        sub  esp, 08h                   ; 0x08 = 8, porque se usan 8 lineas (y ya es mul.4)

        mov byte ptr [ebp-09h], 63h     ; c
        mov byte ptr [ebp-08h], 61h     ; a
        mov byte ptr [ebp-07h], 6Ch     ; l
        mov byte ptr [ebp-06h], 63h     ; c
        mov byte ptr [ebp-05h], 2Eh     ; .
        mov byte ptr [ebp-04h], 65h     ; e
        mov byte ptr [ebp-03h], 78h     ; x
        mov byte ptr [ebp-02h], 65h     ; e

        lea eax, [ebp-09h]              ; Ultima posicion de 'calc.exe' (ebp - 09h)

        push eax
        mov  ebx, 0x77c293c7            ; Direccion de la libreria 'system'
        call ebx
    }
}

