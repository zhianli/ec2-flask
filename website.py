import socket
from flask import Flask,request,make_response,g,request

app = Flask(__name__)

server_ip = socket.gethostbyname(socket.gethostname()) # https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib

@app.before_request
def set_global_value():
    # set the client IP, Port and protocol
    g.client_ip = request.remote_addr # https://www.adamsmith.haus/python/answers/how-to-get-an-ip-address-using-flask-in-python
    g.client_port = request.environ.get('REMOTE_PORT') # https://stackoverflow.com/questions/34785337/how-to-use-flask-get-clients-port
    g.protocol = request.environ.get('SERVER_PROTOCOL')
    
    # get the HTTP request header
    # g.request_headers = '<br>'.join([f'{header[0]}: {header[1]}' for header in request.headers.items()])

    #generic response to show client IP, Port, protocol and server IP
    g.response = f"<p>client ip: {g.client_ip} <br> client port: {g.client_port} <br> server ip: {server_ip} <br> protocol: {g.protocol} </p>"

@app.route("/")
def index():
    response = make_response(f"{g.response}")
    return response

@app.route('/<http_status>')
def return_http_status(http_status):
    response = make_response(f"{g.response} <b> Status Code:</b> {http_status}</p>")
    return response, http_status

@app.route('/headers')
def headers():
    headers = request.headers
    sorted_headers = sorted(headers.items(), key=lambda x: x[0].lower())
    headers_str = '<br>'.join(f'{key}: {value}' for key, value in sorted_headers)
    return headers_str

@app.route('/cookies')
def cookies():
    cookie_header = request.headers.get('Cookie')
    if cookie_header:
        cookies = dict(x.strip().split('=') for x in cookie_header.split(';'))
        my_cookie = cookies.get('my_cookie')
        if my_cookie:
            return f'The value of my_cookie is {my_cookie}'
        else:
            return 'The my_cookie cookie is not present in the request'
    else:
        return 'No cookies were sent with the request'

if __name__ == "__main__":
    app.run(host=server_ip, port=80)