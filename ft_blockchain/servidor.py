from blockchain import Blockchain
from flask      import Flask, jsonify
from uuid       import uuid4


# ----------------------------------------------------------------------------------------------------------------------


# Instanciar un nodo.
aplicacion = Flask(__name__)

# Generar una dirección global y única.
id = str(uuid4()).replace('-', '')

# Crear una nueva blockchain.
b = Blockchain()


# Definir la ruta de minado de una petición GET de la API.
@aplicacion.route('/mine', methods=['GET'])
def minar():
    """
    Mina un nuevo bloque y lo agrega a la blockchain.
    """

    return None

# Definir la ruta de creación de transacciones de una petición POST de la API.
@aplicacion.route('/transactions/new', methods=['POST'])
def nueva_transaccion():
    """
    Crea una nueva transacción y la agrega a la blockchain.
    """

    return None

# Definir la ruta de consulta de la blockchain de una petición GET de la API.
@aplicacion.route('/chain', methods=['GET'])
def cadena_completa():
    """
    Muestra el estado actual de la blockchain.

    :return: cadena de bloques.
    """

    response = {
        'cadena': b.cadena,
        'nodos': len(b.cadena),
    }

    return jsonify(response), 200


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    """
    Arrancar el servidor.
    """
    
    # Servidor alojado en 'localhost:5555'.
    aplicacion.run(host='0.0.0.0', port=5555)
