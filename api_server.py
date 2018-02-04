"""
This is the API-REST server that allows to access the block chain object
"""
from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import BlockChain

PORT = 5000


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Block chain
block_chain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    Our mining endpoint is where the magic happens, and it’s easy. It has to do three things:
    - Calculate the Proof of Work
    - Reward the miner (us) by adding a transaction granting us 1 coin
    - Forge the new Block by adding it to the chain

    Note that the recipient of the mined block is the address of our node.
    And most of what we’ve done here is just interact with the methods on our Block chain class.
    """
    # We run the proof of work algorithm to get the next proof...
    last_block = block_chain.last_block
    last_proof = last_block['proof']
    proof = block_chain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    block_chain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # Forge the new Block by adding it to the chain
    previous_hash = block_chain.hash(last_block)
    block = block_chain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    """
    This is what the request for a transaction will look like. It’s what the user sends to the server:

        {
         "sender": "my address",
         "recipient": "someone else's address",
         "amount": 5
        }

    Since we already have our class method for adding transactions to a block, the rest is easy.
    :return: response in json, 201
    """
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = block_chain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    """

    :return:
    """
    response = {
        'chain': block_chain.chain,
        'length': len(block_chain.chain),
    }
    return jsonify(response), 200


@app.route('/es_el_mercado_amigo', methods=['GET'])
def es_el_mercado_amigo():
    """
    Function to check if this API is the one we're looking for from the outside
    :return: Json response
    """
    response = {
        'message': True,
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """

    :return:
    """
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        block_chain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(block_chain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """

    :return:
    """
    replaced = block_chain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': block_chain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': block_chain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=PORT)
