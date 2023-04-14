# Objetivo

Crear una **blockchain** basada en una prueba de trabajo (*Proof of work*); para ello, se implementará la **lógica de la cadena de bloques**, así como un **servidor** a través del cual se pueda interactuar con la misma.

Este proyecto permite utilizar:

- Cualquier lenguaje de programación. 
- Se puede utilizar librerías criptográficas como *openssl* o *hashlib* para la generación de hashes, pero la estructura de la cadena de bloques debe ser implementada por mí.
- Un framework web como *NestJS* o *Flask* para la implementación del servidor.


## Requisitos

La blockchain debe cumplir lo siguiente:

- [x] El flujo de trabajo debe ser: añadir transacciones al bloque actual y minar el bloque para añadirlo a la cadena.
- [x] El algoritmo de la prueba de trabajo (PoW) debe ser simple.
- [x] La cadena de bloques no será persistente, es decir, se almacenará en la memoria del servidor, sin base de datos.
- [x] Una vez creada la blockchain, se podrá interactuar con ella usando peticiones HTTP:

| Petición |          Dirección           | Acción                                                                          |
|:--------:|:----------------------------:|:------------------------------------------------------------------------------- |
|   POST   | $\texttt{/transactions/new}$ | Envía una nueva transacción para añadir al próximo bloque.                      |
|   GET    |       $\texttt{/mine}$       | Ejecuta la prueba de trabajo y crea un nuevo bloque.                            |
|   GET    |      $\texttt{/chain}$       | Devuelve la información sobre la cadena de bloques (bloques, transacciones...). |

> [!NOTE]
> Mi *PoW* consiste en comprobar que el hash obtenido termina en $\texttt{42}$.  
> Cada 10 bloques se añade un $\texttt{42}$ más a la comprobación ($\texttt{42}$, $\texttt{4242}$, $\texttt{424242}$, ...).

El desarrollo de la minería debe cumplir lo siguiente:  
- [x] Calcular la prueba de trabajo (*PoW*).
- [x] Recompensar a los mineros (una transacción).  
- [x] Creación del nuevo bloque y añadirlo a la cadena.


# Funcionamiento

El proyecto consta de 2 archivos: *blockchain.py*, que implementa una clase para la cadena de bloques; y *servidor.py*, que usa dicha clase para implementar un servidor de minado y por tanto, es el único archivo ejecutable.


## Ejecutar el *servidor*

Para ejecutar el servidor, se debe ejecutar el siguiente comando:

```bash
python3 servidor.py
```

## Interactuar con el *servidor*

Una vez ejecutado el servidor, se puede interactuar con él usando peticiones HTTP; para ello, se puede usar $\texttt{curl}$ o cualquier otro cliente HTTP (en mi caso, usé Postman) para enviar peticiones a los endpoints definidios en los [requisitos](#requisitos).

El servidor escuchará localmente en el puerto 5555, por lo que se interactuará con él en la dirección *[localhost:5555](http://localhost:5555)* en todo momento.

> [!NOTE]
> El número del puerto es una referencia a *Daft Punk*.


### Minar un bloque

Se debe enviar una *petición GET* a *[localhost:5555/mine](http://localhost:5555/mine)*.

En caso de éxito, se obtendrá una respuesta con el siguiente formato:

```json
{
    "hash anterior": "257ed03d7eef77c51f7ee3494e2463b58df6c48d79eedb39ce0ddb18395737fd",
    "prueba": 169,
    "timestamp": 1662992152.5854888,
    "transacciones": [
        {
            "cantidad": 1,
            "emisor": 0,
            "receptor": "f9f89273a2004245b4f8bcf0cb4c8df8"
        }
    ],
    "índice":2
}
```

> [!IMPORTANT]
> Un bloque siempre tendrá una transacción como mínimo: la recompensa al minero.


### Añadir una transacción

Se debe enviar una *petición POST* a *[localhost:5555/transactions/new](http://localhost:5555/transactions/new)* con el siguiente formato:

```json
{
    "emisor": "dirección del emisor",
    "receptor": "dirección del receptor",
    "cantidad": 5
}
```

En caso de éxito, se devolverá un código 200 y un mensaje:

```json
{
    "mensaje": "Transacción añadida al bloque X."
}
```

> [!IMPORTANT]
> $X$ es el último bloque de la Blockchain que se esté minando.  
> Es decir, el siguiente en añadirse a la cadena.


### Obtener la cadena de bloques

Se debe enviar una *petición GET* a *[localhost:5555/chain](http://localhost:5555/chain)*.

En caso de éxito, se devolverá un código 200 y un mensaje con el siguiente formato:

```json
{
    "cadena": [
        {
            "anterior": null,
            "prueba": 1,
            "timestamp": 1662992139.5264525,
            "transacciones": [],
            "índice": 1
        },
        {
            "anterior": "257ed03d7eef77c51f7ee3494e2463b58df6c48d79eedb39ce0ddb18395737fd",
            "prueba": 169,
            "timestamp": 1662992152.5854888,
            "transacciones": [
                {
                    "cantidad": 1,
                    "emisor": 0,
                    "receptor": "f9f89273a2004245b4f8bcf0cb4c8df8"
                }
            ],
            "índice": 2
        },
        {
            "anterior": "72ec7e78f59843e7e6dc23ca937c11129b2a8bc2cb63d14efbe70596bd628d67",
            "prueba": 338,
            "timestamp": 1662992816.2664776,
            "transacciones": [
                {
                    "cantidad": 10,
                    "emisor": "0123456789",
                    "receptor": "9876543210"
                },
                {
                    "cantidad": 10,
                    "emisor": "572576272546257",
                    "receptor": "987654542624563210"
                },
                {
                    "cantidad": 15,
                    "emisor": "545645153223",
                    "receptor": "233242345324"
                },
                {
                    "cantidad": 5,
                    "emisor": "980678058694794783",
                    "receptor": "1234537760869"
                },
                {
                    "cantidad": 1,
                    "emisor": 0,
                    "receptor": "f9f89273a2004245b4f8bcf0cb4c8df8"
                }
            ],
            "índice": 3
        }
    ],
    "nodos": 3
}
```

> [!NOTE]
> Recomiendo usar la aplicación online [JSON CRACK](https://jsoncrack.com) (antes *JSON Visio*), que permite visualizar los archivos JSON de una forma muy cómoda.


## Registro y resolución de nodos

Como apartado bonus del proyecto, se proponía implementar una verdadera descentralización permitiendo que existieran múltiples nodos en la red, implementando:

- Un sistema de **registro de nodos**, que permitía a los nodos notificar a la red sobre su participación en la Blockchain.
- Un sistema de **resolución de conflictos**, que permitía a los nodos resolver diferencias entre cadenas de bloques, en caso de que existieran.

> [!WARNING]
> Ambas funcionalidades están implementadas en el proyecto.  
> Sin embargo, **la resolución de conflictos no funciona correctamente**, por eso no he añadido ninguna descripción de dichas funcionalidades.
