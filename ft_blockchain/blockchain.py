from time import time


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
        self.crear_bloque(anterior=0, prueba=100)   # Valores por defecto (genesis)


    def crear_bloque(self, anterior=None, prueba=None):
        """
        Crea un nuevo bloque y lo agrega a la cadena de bloques.

        :param anterior: índice del bloque anterior.
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
        return self.ultimo_bloque['index'] + 1


    @staticmethod
    def computar_hash(bloque):
        """
        Calcula el hash de un bloque.

        :param bloque: Bloque al que calcularle el hash.
        """
        pass


    @property
    def ultimo_bloque(self):
        """
        :return: El último bloque de la cadena de bloques.
        """
        
        return self.cadena[-1]
    