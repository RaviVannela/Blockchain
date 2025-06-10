from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    proof = blockchain.proof_of_work(previous_block['proof'])
    blockchain.add_transaction(sender='system', receiver='node1', amount=1)
    block = blockchain.create_block(proof, blockchain.hash(previous_block))
    return jsonify(block), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.form
    index = blockchain.add_transaction(data['sender'], data['receiver'], float(data['amount']))
    return f'Transaction will be added to Block {index}', 201

@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify(chain=blockchain.chain, length=len(blockchain.chain)), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)
