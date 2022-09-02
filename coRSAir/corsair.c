/*
 * Extracción de los datos de la clave privada
 * usando 2 certificados RSA que comparten un
 * número primo 'p' en su construcción.
 */


#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <stdio.h>

// Librerías necesarias para este proyecto (OpenSSL)
#include <openssl/bn.h>
#include <openssl/rsa.h>
#include <openssl/bio.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/x509.h>

#define BUFFER 1024


/**
 * Método principal.
 *
 * @return  0 si correcto.
 */
int main(int argc, char *argv[]) {
    return 0;
}
