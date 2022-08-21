import json

from time import time
from hashlib import sha256


# ----------------------------------------------------------------------------------------------------------------------


class Blockchain(object):
    """
    Clase que representa una Blockchain.
    Gestiona una lista de transacciones y de bloques, simulando
    el funcionamiento real de una blockchain, pero a menor escala.
    """

    def __init__(self):
        """
        Inicializa la blockchain con un bloque genesis.
        """

        # Inicializar una blockchain vacía.
        self.cadena = []
        self.transacciones = []

        # Crear el bloque genesis.
        self.crear_bloque(anterior=None, prueba=1)   # Valores por defecto (genesis)


    def crear_bloque(self, anterior=None, prueba=None):
        """
        Crea un nuevo bloque y lo agrega a la cadena de bloques.

        :param anterior: hash del bloque anterior.
        :param prueba: valor de la prueba (PoW) para el nuevo bloque.
        """

        # Crear un nuevo bloque.
        bloque = {
            'índice': len(self.cadena) + 1,
            'timestamp': time(),
            'transacciones': self.transacciones,
            'prueba': prueba,
            'anterior': anterior
        }

        # Agregar el bloque a la cadena.
        self.cadena.append(bloque)

        # Limpiar la cadena de transacciones.
        self.transacciones = []

        # Devolver el bloque recién creado.
        return bloque

    def crear_transaccion(self, emisor, receptor, cantidad):
        """
        Crea una nueva transacción y la agrega a la cadena de transacciones.

        :param emisor: dirección del emisor.
        :param receptor: dirección del receptor.
        :param cantidad: cantidad enviada del emisor al receptor.

        :return: índice del bloque que contendrá esta transacción.
        """

        # Crear una nueva transacción.
        transaccion = {
            'emisor': emisor,
            'receptor': receptor,
            'cantidad': cantidad
        }

        # Agregar la transacción a la cadena.
        self.transacciones.append(transaccion)

        # Devolver el índice del siguiente bloque a ser minado.
        return self.ultimo_bloque['índice'] + 1

    @staticmethod
    def computar_hash(bloque):
        """
        Calcula el hash de un bloque usando SHA256.

        :param bloque: Bloque al que calcularle el hash.

        :return: Hash del bloque en formato hexadecimal.
        """

        # Convertir el bloque (en formato JSON) a un 'str'.
        bloque_s = json.dumps(bloque, sort_keys=True).encode()

        # Calcular el hash del bloque.
        return sha256(bloque_s).hexdigest()

    @property
    def ultimo_bloque(self):
        """
        :return: El último bloque de la cadena de bloques.
        """

        return self.cadena[-1]

    def prueba_trabajo(self, anterior):
        """
        Calcula la prueba de trabajo para un nuevo bloque usando
        un número 'y' tal que 'hash(x·y)' termina en '42'; donde
        'x' es la prueba anterior e 'y' es la prueba actual.
        Cada 10 bloques minados, se añade un '42' necesario al
        final del hash (es decir, '42', '4242', '424242'...).
        """
        
        prueba = anterior      # Contador
        final = '42' * (1 + len(self.cadena) // 10)     # Final de la prueba

        # Calcular la prueba de trabajo.
        print(prueba, sha256(f'{anterior * prueba}'.encode()).hexdigest(), final)
        while not sha256(f'{anterior * prueba}'.encode()).hexdigest().endswith(final):
            prueba += 1
            print(prueba, sha256(f'{anterior * prueba}'.encode()).hexdigest(), final)

        # Devolver la prueba de trabajo.
        return prueba
