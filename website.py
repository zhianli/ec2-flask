import socket
from flask import Flask,request

app = Flask(__name__)

server_ip = socket.gethostbyname(socket.gethostname()) # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

@app.route("/")
def index():
    client_ip = request.remote_addr # https://www.adamsmith.haus/python/answers/how-to-get-an-ip-address-using-flask-in-python
    client_port = request.environ.get('REMOTE_PORT') # https://stackoverflow.com/questions/34785337/how-to-use-flask-get-clients-port
    protocol = request.environ.get('SERVER_PROTOCOL')
    return f"<p>client ip: {client_ip} <br> client port: {client_port} <br> server ip: {server_ip} <br> protocol: {protocol}</p>", 200


if __name__ == "__main__":
    app.run(host=server_ip, port=80)