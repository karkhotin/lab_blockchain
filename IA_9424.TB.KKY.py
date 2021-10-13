import hashlib
import json
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
from textwrap import dedent
class Blockchain(object):
    def __init__(self):
        self.chain_KKY = []
        self.current_transactions_KKY = []
        self.new_block_KKY(previous_hash=1, proof=9122001)

    def new_block_KKY(self, proof, previous_hash=None):
        block_KKY = {
            'index': len(self.chain_KKY) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions_KKY,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_KKY(self.chain_KKY[-1]),
        }
        self.current_transactions_KKY = []
        self.chain_KKY.append(block_KKY)
        return block_KKY

    def new_transaction_KKY(self, sender, recipient, amount):
        self.current_transactions_KKY.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        print('amount', amount)
        return self.last_block['index'] + 1

    def proof_of_work_KKY(self, last_proof):
        proof_KKY = 0
        while self.valid_proof_KKY(last_proof, proof_KKY) is False:
            proof_KKY += 1
        return proof_KKY

    @staticmethod
    def valid_proof_KKY(last_proof, proof):
        guess_KKY = f'{last_proof}{proof}'.encode()
        guess_hash_KKY = hashlib.sha256(guess_KKY).hexdigest()
        if (guess_hash_KKY[-2:]=="12"):
            print(guess_hash_KKY)
        return guess_hash_KKY[-2:] == "12"

    def hash_KKY(self, block):
        block_string_KKY = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string_KKY).hexdigest()

    @property
    def last_block(self):
        return self.chain_KKY[-1]

app = Flask(__name__)
node_id = str(uuid4()).replace('-', '')
blockchain = Blockchain()
print(blockchain.proof_of_work_KKY(9122001))
print(blockchain.proof_of_work_KKY(9122))
@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work_KKY(last_proof)
    blockchain.new_transaction_KKY(
        sender="0",
        recipient=node_id,
        amount=9,
    )

    previous_hash = blockchain.hash_KKY(last_block)
    block = blockchain.new_block_KKY(proof, previous_hash)
    block_hash=blockchain.hash_KKY(block)
    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'hash': block_hash,
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction_KKY():
 values = request.get_json()
 required = ['sender', 'recipient', 'amount']
 if not all(k in values for k in required):
     return 'Missing values', 400
 index = blockchain.new_transaction_KKY(values['sender'], values['recipient'], values['amount'])
 response = {'message': f'Transaction will be added to Block {index}'}
 return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain_KKY,
        'length': len(blockchain.chain_KKY),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

