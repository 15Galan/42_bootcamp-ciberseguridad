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
    // Definir las variables necesarias para el programa
    unsigned char *res;     // Buffer para los resultados
    unsigned char *sol;     // Buffer para la solución

    BN_CTX *ctx;        // Contexto para el algoritmo RSA
    RSA *privada;       // Clave privada RSA
    BIO *bioprint;      //
    BIGNUM *one;        // Número '1' en formato 'BIGNUM'

    RSA *rsa1;          //               ╭ Clave pública
    BIGNUM *n1;         // Certificado 1 ┼ Número primo 'n'
    BIGNUM *q1;         //               ╰ Número primo 'q'

    RSA *rsa2;          //               ╭ Clave pública
    BIGNUM *n2;         // Certificado 2 ┼ Número primo 'n'
    BIGNUM *q2;         //               ╰ Número primo 'q'

    BIGNUM *p;          // Número primo 'p' común a los dos certificados

    BIGNUM *total;      // Número total de los dos certificados
    BIGNUM *fi1;        // Número de factores primos de 'n'
    BIGNUM *fi2;        // Número de factores primos de 'n'

    BIGNUM *e;          // Exponente de la clave pública
    BIGNUM *d;          // Exponente de la clave privada

    int fd;             // Descriptor del archivo de entrada
    int len;            // Longitud del archivo de entrada

    // Inicializar las variables
    res = malloc(sizeof(unsigned char) * BUFFER);
    sol = malloc(sizeof(unsigned char) * BUFFER);

    ctx = BN_CTX_new();

    bioprint = BIO_new_fp(stdout, BIO_NOCLOSE);

    // Obtener RSA 1
    // Obtener RSA 2

    one = BN_new();

    q1 = BN_new();
    q2 = BN_new();

    p = BN_new();
    d = BN_new();

    total = BN_new();
    fi1 = BN_new();
    fi2 = BN_new();

    privada = RSA_new();

    return 0;
}
