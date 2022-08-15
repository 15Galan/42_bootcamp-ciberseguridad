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


    def crear_transaccion(self):
        """
        Crea una nueva transacción y la agrega a la cadena de transacciones.
        """
        pass


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
    