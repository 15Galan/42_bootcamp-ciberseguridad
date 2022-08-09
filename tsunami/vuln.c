#include <string.h>


/**
 * Programa vulnerable que demuestra el funcionamiento
 * (y los resultados) de un desbordamiento de buffer.
 *
 * Aquí se presenta un buffer de 64 bytes al que se le asigna un valor
 * superior a 64 bytes, la cadena 'AAAABBBBCCCC ... TTTTUUUUVVVV'. Esto
 * provoca se desborde en la seccion 'RRRR', ya que se han suprado 64 bytes.
 */
int	main(int argc, char **argv) {
    char buffer[64];

    strcpy(buffer, argv[1]);
    // strcpy(buffer, "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQQ");
    // Se produce el desbordamiento con salida 'Offset: 52525252'; es decir, con la secuencia 'RRRR'.
    // Se produce error de ejecución con salida 'Offset: 00001200' si se deja hasta '···QQQQ'.

    return 0;
}

