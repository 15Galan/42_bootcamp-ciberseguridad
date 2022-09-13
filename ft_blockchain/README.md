# Objetivo

Crear una **blockchain** basada en una prueba de trabajo (*Proof of work*); para ello, se implementará la **lógica de la
cadena de bloques**, así como un **servidor** a través del cual se pueda interactuar con la misma.

Este proyecto permite utilizar:
- Cualquier lenguaje de programación. 
- Se puede utilizar librerías criptográficas como `openssl` o `hashlib` para la generación de hashes, pero la 
estructura de la cadena de bloques debe ser implementada por mí.
- Un framework web como `NestJS` o `Flask` para la implementación del servidor.


## Requisitos

La blockchain debe cumplir lo siguiente:
- [x] El flujo de trabajo debe ser: añadir transacciones al bloque actual y minar el bloque para añadirlo a la cadena.
- [x] El algoritmo de la prueba de trabajo (PoW) debe ser simple.
- [x] La cadena de bloques no será persistente, es decir, se almacenará en la memoria del servidor, sin base de datos.
- [x] Una vez creada la blockchain, se podrá interactuar con ella usando peticiones HTTP:
	- [x] POST `/transactions/new`: Envía una nueva transacción para añadir al próximo bloque.
	- [x] GET `/mine`: Ejecuta la prueba de trabajo y crea un nuevo bloque.  
	- [x] GET `/chain`: Devuelve la información sobre la cadena de bloques (bloques, transacciones...).

* Mi _PoW_ consiste en comprobar que el hash obtenido termina en `42`, añadiendo un `42` más cada 10 bloques.

El desarrollo de la minería debe cumplir lo siguiente:  
- [x] Calcular la prueba de trabajo (_PoW_).
- [x] Recompensar a los mineros (una transacción).  
- [x] Creación del nuevo bloque y añadirlo a la cadena.


# Funcionamiento

El proyecto consta de 2 archivos: `blockchain.py`, que implementa una clase para la cadena de bloques; y `servidor.py`,
que usa dicha clase para implementar un servidor de minado y por tanto, es el único archivo ejecutable.

## Ejecutar el `servidor`

Para ejecutar el servidor, se debe ejecutar el siguiente comando:

```bash
python3 servidor.py
```

## Interactuar con el `servidor`

Una vez ejecutado el servidor, se puede interactuar con él usando peticiones HTTP; para ello, se puede usar `curl` o
cualquier otro cliente HTTP (en mi caso, usé Postman) para enviar peticiones a los endpoints definidios en los
[requisitos](#requisitos).

El servidor escuchará localmente en el puerto `5555`, por lo que se interactuará con él en la dirección
`http://localhost:5555` en todo momento.


### Minar un bloque

Se debe enviar una petición `GET` a `http://localhost:5555/mine`.

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
- Un bloque siempre tendrá como mínimo, una transacción: la recompensa al minero.


### Añadir una transacción

Se debe enviar una petición `POST` a `http://localhost:5555/transactions/new` con el siguiente formato:

```json
{
	"emisor": "dirección del emisor",
	"receptor": "dirección del receptor",
	"cantidad": 5
}
```

En caso de éxito, se devolverá un código `200` y un mensaje:

```json
{
	"mensaje": "Transacción añadida al bloque X."
}
```
- Siendo $X$ el último bloque de la Blockchain que se esté minando (es decir, el siguiente en añadirse a la cadena).


### Obtener la cadena de bloques

Se debe enviar una petición `GET` a `http://localhost:5555/chain`.

En caso de éxito, se devolverá un código `200` y un mensaje con el siguiente formato:

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
- Recomiendo usar la aplicación online [JSON Visio](https://jsoncrack.com/editor?json=%5B%5B%22cadena%22%2C%22nodos%22%2C%22a%7C0%7C1%22%2C%22anterior%22%2C%22prueba%22%2C%22timestamp%22%2C%22transacciones%22%2C%22%C3%ADndice%22%2C%22a%7C3%7C4%7C5%7C6%7C7%22%2C%22n%7C1%22%2C%22n%7C1oXkDr.M2y1%22%2C%22a%7C%22%2C%22o%7C8%7C%7C9%7CA%7CB%7C9%22%2C%22257ed03d7eef77c51f7ee3494e2463b58df6c48d79eedb39ce0ddb18395737fd%22%2C%22n%7C2j%22%2C%22n%7C1oXkE4.bHHl%22%2C%22cantidad%22%2C%22emisor%22%2C%22receptor%22%2C%22a%7CG%7CH%7CI%22%2C%22n%7C0%22%2C%22f9f89273a2004245b4f8bcf0cb4c8df8%22%2C%22o%7CJ%7C9%7CK%7CL%22%2C%22a%7CM%22%2C%22n%7C2%22%2C%22o%7C8%7CD%7CE%7CF%7CN%7CO%22%2C%2272ec7e78f59843e7e6dc23ca937c11129b2a8bc2cb63d14efbe70596bd628d67%22%2C%22n%7C5S%22%2C%22n%7C1oXkOm.SQOk%22%2C%22n%7CA%22%2C%220123456789%22%2C%229876543210%22%2C%22o%7CJ%7CT%7CU%7CV%22%2C%22572576272546257%22%2C%22987654542624563210%22%2C%22o%7CJ%7CT%7CX%7CY%22%2C%22n%7CF%22%2C%22545645153223%22%2C%22233242345324%22%2C%22o%7CJ%7Ca%7Cb%7Cc%22%2C%22n%7C5%22%2C%22980678058694794783%22%2C%221234537760869%22%2C%22o%7CJ%7Ce%7Cf%7Cg%22%2C%22a%7CW%7CZ%7Cd%7Ch%7CM%22%2C%22n%7C3%22%2C%22o%7C8%7CQ%7CR%7CS%7Ci%7Cj%22%2C%22a%7CC%7CP%7Ck%22%2C%22o%7C2%7Cl%7Cj%22%5D%2C%22m%22%5D).


## Registro y resolución de nodos

Como apartado bonus del proyecto, se proponía implementar una verdadera descentralización permitiendo que existieran
múltiples nodos en la red, implementando: un sistema de registro de nodos, que permitía a los nodos notificar a la red
sobre su participación en la Blockchain; un sistema de resolución de conflictos, que permitía a los nodos resolver
diferencias entre cadenas de bloques, en caso de que existieran.

Estas 2 funcionalidades están implementadas en el proyecto, pero **la resolución de conflictos no funciona correctamente**,
por eso no he añadido ninguna descripción de dichas funcionalidades.