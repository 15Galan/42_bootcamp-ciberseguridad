class Blockchain(object):

    def __init__(self):
        """
        Inicializa la blockchain con un bloque genesis.
        """

        self.cadena = []
        self.transacciones = []


    def crear_bloque(self):
        """
        Crea un nuevo bloque y lo agrega a la cadena de bloques.
        """
        pass


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
    