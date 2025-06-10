import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.nodes = set()
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        while True:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                return new_proof
            new_proof += 1

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        for i in range(1, len(chain)):
            prev = chain[i-1]
            current = chain[i]
            if current['previous_hash'] != self.hash(prev):
                return False
            if not self.valid_proof(prev['proof'], current['proof']):
                return False
        return True

    def valid_proof(self, previous_proof, proof):
        guess = f'{proof**2 - previous_proof**2}'.encode()
        return hashlib.sha256(guess).hexdigest()[:4] == "0000"

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 'receiver': receiver, 'amount': amount})
        return self.get_previous_block()['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        longest_chain = self.chain
        max_length = len(longest_chain)

        for node in self.nodes:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                data = response.json()
                if data['length'] > max_length and self.is_chain_valid(data['chain']):
                    max_length = data['length']
                    longest_chain = data['chain']
        
        if longest_chain != self.chain:
            self.chain = longest_chain
            return True
        return False
