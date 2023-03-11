import socket
from flask import Flask,request,make_response,g,request,abort

app = Flask(__name__)

server_ip = socket.gethostbyname(socket.gethostname()) # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

@app.before_request
def set_global_value():

    # set the client IP, Port and protocol
    g.client_ip = request.remote_addr # https://www.adamsmith.haus/python/answers/how-to-get-an-ip-address-using-flask-in-python
    g.client_port = request.environ.get('REMOTE_PORT') # https://stackoverflow.com/questions/34785337/how-to-use-flask-get-clients-port
    g.protocol = request.environ.get('SERVER_PROTOCOL')
    
    #generic response to show client IP, Port, protocol and server IP
    g.response = f"<p>client ip: {g.client_ip} <br> client port: {g.client_port} <br> server ip: {server_ip} <br> protocol: {g.protocol} </p>"

@app.route("/")
def index():
    response = make_response(f"{g.response}")
    return response

@app.route('/status/<int:status_code>')
def return_status(status_code):
    if status_code < 200 or status_code >= 600:
        abort(404)
    return f"Status code: {status_code}", status_code

@app.route('/headers')
def headers():
    headers = []
    for header in sorted(request.headers.keys()):
        headers.append(f'{header}: {request.headers.get(header)}')
    return '<br>'.join(headers)

if __name__ == "__main__":
    app.run(host=server_ip, port=80)