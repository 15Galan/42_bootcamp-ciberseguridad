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
 * Cargar un certificado RSA desde un archivo.
 *
 * @param fichero   Ruta del archivo.
 *
 * @return  Clave RSA cargada.
 */
RSA *obtener_rsa(char *fichero) {
    // Definir las variables
    X509 *cert;                 // Certificado
    EVP_PKEY *pkey;             // Clave pública
    RSA *rsa;                   // Clave RSA
    BIO *bio;                   // Buffer de entrada
    int correcto;               // Indicador de lectura correcta

    // Inicializar las variables
    bio = BIO_new(BIO_s_file());                    // Crear el buffer de entrada
    correcto = BIO_read_filename(bio, fichero);     // Abrir el archivo

    // Comprobar que el fichero se leyó correctamente
    if (correcto != 1) {
        printf("Error al leer el fichero '%s'.\n", fichero);
        exit(1);
    }

    // Leer el certificado
    cert = PEM_read_bio_X509(bio, NULL, 0, NULL);   // Leer el certificado
    pkey = X509_get_pubkey(cert);                   // Obtener la clave pública
    rsa = EVP_PKEY_get1_RSA(pkey);                  // Obtener la clave RSA

    // Liberar la memoria
    X509_free(cert);        // Liberar el certificado
    EVP_PKEY_free(pkey);    // Liberar la clave pública
    BIO_free(bio);          // Liberar el buffer de entrada

    return rsa;
}

/**
 * Método principal.
 *
 * @return  0 si correcto.
 */
int main(int argc, char *argv[]) {
    // Definir las variables
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

    rsa1 = obtener_rsa(argv[1]);
    rsa2 = obtener_rsa(argv[2]);

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
