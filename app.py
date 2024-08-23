
from flask import Flask, render_template, request
from flask_sockets import Sockets
import random
import string

app = Flask(__name__)
sockets = Sockets(app)

# Store host and client addresses
host_address = None
client_address = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/host', methods=['POST'])
def host():
    global host_address
    host_address = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return {'address': host_address}

@app.route('/client', methods=['POST'])
def client():
    global client_address
    client_address = request.json.get('address')
    if client_address == host_address:
        return {'status': 'connected'}
    return {'status': 'failed'}

@sockets.route('/stream')
def stream(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            ws.send(message)

if __name__ == '__main__':
    app.run(port=5000)
