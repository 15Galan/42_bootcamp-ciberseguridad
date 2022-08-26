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
    b.crear_transaccion(0, id, 1 + len(b.cadena) // 10)

    """
    Se usa el emisor '0' (genesis) para representar una transacción de recompensa.
    La recompensa de esta prueba de concepto es 1 unidad por cada 10 bloques existentes.
    """

    # Crear el nuevo bloque.
    bloque = b.crear_bloque(b.computar_hash(ultimo_bloque), prueba)

    # Respuesta de la petición HTTP.
    respuesta = {
        'timestamp': bloque['timestamp'],
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


# Definir la ruta de consulta de la blockchain de una petición POST de la API.
@aplicacion.route('/nodes/register', methods=['POST'])
def registrar_nodo():
    """
    Registra un nuevo nodo en la cadena de bloques.
    """

    # Obtener los datos de la petición.
    valores = request.get_json()

    # Verificar que los datos de la petición sean válidos.
    if 'nodo' not in valores:
        return jsonify({'error': 'La petición no tiene nodo.'}), 400

    # Agregar el nodo a la cadena de bloques.
    b.agregar_nodo(valores['nodo'])

    # Respuesta de la petición HTTP.
    respuesta = {
        'mensaje': 'Nodo agregado',
        'cadena de nodos': b.cadena
    }

    return jsonify(respuesta), 201


@aplicacion.route('/nodes/resolve', methods=['GET'])
def resolver_nodos():
    """
    Resuelve los nodos en la cadena de bloques.
    """

    # Resolver la cadena de bloques.
    reemplazo = b.resolver_conflictos()

    # Respuesta de la petición HTTP.
    if reemplazo:
        respuesta = {
            'mensaje': 'La cadena de bloques se ha reemplazado.',
            'nueva cadena de bloques': b.cadena
        }

    else:
        respuesta = {
            'mensaje': 'La cadena de bloques está actualizada.',
            'cadena de bloques': b.cadena
        }

    return jsonify(respuesta), 200


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
