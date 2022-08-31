import json
import requests

from time           import time
from hashlib        import sha256
from urllib.parse   import urlparse


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
        self.nodos = set()
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

        
    def crear_nodo(self, direccion):
        """
        Crea un nuevo nodo y lo añade al conjunto de nodos.

        :param direccion: Dirección del nodo.
        """

        self.nodos.add(urlparse(direccion).netloc)


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

        :return:    Prueba de trabajo para el nuevo bloque.
        """
        
        prueba = anterior                               # Contador
        final = '42' * (1 + len(self.cadena) // 10)     # Final de la prueba

        # Definición local del cálculo del hash.
        def hash(anterior, prueba):
            return sha256(f'{anterior * prueba}'.encode()).hexdigest()

        # Calcular la prueba de trabajo.
        print(prueba, hash(anterior, prueba), final)

        while not hash(anterior, prueba).endswith(final):
            prueba += 1

            print(prueba, hash(anterior, prueba), final)

        # Devolver la prueba de trabajo.
        return prueba


    def validar_prueba(self, anterior, actual):
        """
        Determina si una prueba es válida.
        
        :param anterior:    Prueba anterior.
        :param actual:      Prueba actual.

        :return:            True si la prueba es válida; False en caso contrario.
        """

        # Calcular la prueba de trabajo.
        final = '42' * (1 + len(self.cadena) // 10)     # Final de la prueba

        # Determinar si la prueba es válida.
        return sha256(f'{anterior * actual}'.encode()).hexdigest().endswith(final)


    def validar_cadena(self, cadena):
        """
        Determina si una cadena es válida.

        :param cadena:  Cadena a validar.

        :return:        True si es válida; False en caso contrario.
        """

        # Inicializar las variables.
        ultimo_bloque = cadena[-1]
        indice = 1

        # Comprobar qué cadena
        while indice < len(cadena):
            bloque = cadena[indice]

            # Verificar que el bloque anterior es el correcto.
            if bloque['anterior'] != ultimo_bloque['prueba']:
                return False

            # Verificar que el hash del bloque es correcto.
            if self.computar_hash(bloque) != bloque['hash']:
                return False

            # Actualizar el último bloque.
            ultimo_bloque = bloque

            # Incrementar el índice.
            indice += 1
            
        return True


    def resolver_conflictos(self):
        """
        Resuelve los conflictos de la cadena de bloques,
        reemplazándola por aquella cadena válida más larga.
        Implementación del 'algoritmo de consenso'.

        :return:    True si la cadena de bloques se reemplaza; False en caso contrario.
        """

        # Inicializar variables.
        nodos = self.nodos
        cadena_max = []         # Centinela.
        
        # Comprobar las cadenas de los nodos vecinos.
        for n in nodos:
            try:
                # Crear una petición de la cadena al nodo.
                peticion = requests.get(f'http://{n}/chain')

                if peticion.status_code == 200:

                    # Obtener la cadena del nodo.
                    cadena_nodo = peticion.json()['cadena']

                    # Comprobar si la cadena recibida es válida y más larga.
                    if self.validar_cadena(cadena_nodo) and len(cadena_max) < len(cadena_nodo):
                        # Reemplazar la cadena de bloques.
                        cadena_max = cadena_nodo
                        
            except requests.exceptions.ConnectionError:
                print(f'Error de conexión con el nodo {n}. Ignorando en el consenso.')

        # Reemplazar la cadena de bloques.
        if len(self.cadena) < len(cadena_max):
            self.cadena = cadena_max

            return True

        return False
