import hashlib
import json
from time import time

class Blockchain (object):
    def __init__(self):
        self.chain_KKY = []
        self.current_transactions=[]
        self.new_block_KKY(previous_hash = 'Khotin', proof = '09122001')
    def new_block_KKY(self, proof, previous_hash = None):
        block={
            'index': len(self.chain_KKY)+1,
            'timestamp':time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_KKY(self.chain_KKY[-1])
            }
        self.current_transactions=[]
        self.chain_KKY.append(block)
        return block

    def new_transaction(self, sender,recipient,amount):
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount
            })
        return self.last_block_KKY['index']+1

    def last_block_KKY(self):
        return self.chain_KKY[-1]
    def hash_KKY(block):
        block_str=json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def proof_of_work(self,last_proof):
        proof=0
        while self.valid_proof(last_proof, proof) is False:
            proof+=1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess=f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2]=='01'

blockchain=Blockchain()
block_KKY=blockchain.new_block_KKY(['09122001'],'acfb0932d7fbb22c2704067702a192ab914c6f30277c0e563fae53c3bc55ab6d')
blockchain.proof_of_work(['12'])
print(block_KKY)