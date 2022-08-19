from blockchain import Blockchain
from flask      import Flask, jsonify, request
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

    # Realizar prueba de trabajo (PoW).
    ultimo_bloque = b.ultimo_bloque
    ultima_prueba = ultimo_bloque['prueba']

    prueba = b.prueba_trabajo(ultima_prueba)

    # Generar transacción para recompensar al minero.
    b.crear_transaccion(0, id, 1)

    """
    Se usa el emisor '0' (genesis) para representar una transacción de recompensa.
    La recompensa de este ejemplo es 1 unidad.
    """

    # Crear el nuevo bloque.
    bloque = b.crear_bloque(b.computar_hash(ultimo_bloque), prueba)

    # Respuesta de la petición HTTP.
    respuesta = {
        'mensaje': 'Se ha creado un nuevo bloque.',
        'índice': bloque['índice'],
        'transacciones': bloque['transacciones'],
        'prueba': bloque['prueba'],
        'hash anterior': bloque['anterior']
    }

    return jsonify(respuesta), 201


# Definir la ruta de creación de transacciones de una petición POST de la API.
@aplicacion.route('/transactions/new', methods=['POST'])
def nueva_transaccion():
    """
    Crea una nueva transacción y la agrega a la blockchain.
    """

    # Obtener los datos de la transacción.
    valores = request.get_json()

    # Verificar que los valores de la transacción sean válidos.
    if 'emisor' not in valores:
        return jsonify({'error': 'La transacción no tiene emisor.'}), 400

    elif 'receptor' not in valores:
        return jsonify({'error': 'La transacción no tiene receptor.'}), 400

    elif 'cantidad' not in valores:
        return jsonify({'error': 'La transacción no tiene cantidad.'}), 400

    # Crear una nueva transacción.
    indice = b.crear_transaccion(valores['emisor'], valores['receptor'], valores['cantidad'])

    # Crear una respuesta JSON con el índice del bloque que contendrá la transacción.
    if indice:
        return jsonify({'mensaje': f'Transacción añadida al Bloque {indice}.'}), 201

    else:
        return jsonify({'error': 'Fallo al registrar la transacción.'}), 500


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
