import socket
from flask import Flask, request, make_response, g, abort, url_for

app = Flask(__name__)

server_ip = socket.gethostbyname(socket.gethostname())

@app.before_request
def set_global_value():
    g.client_ip = request.remote_addr
    g.client_port = request.environ.get('REMOTE_PORT')
    g.protocol = request.environ.get('SERVER_PROTOCOL')
    g.response = f"<p>client ip: {g.client_ip} <br> client port: {g.client_port} <br> server ip: {server_ip} <br> protocol: {g.protocol} </p>"

@app.route("/")
def index():
    response = make_response(f"{g.response}")
    return response

# @app.route('/list-routes')
# def list_routes():
#     # Generate an HTML list of all available routes
#     routes = [rule.rule for rule in app.url_map.iter_rules() if 'GET' in rule.methods]
#     html_list = '<ul>'
#     for route in routes:
#         html_list += f"<li>{route}</li>"
#     html_list += '</ul>'
#     return f"<h2>List of Available Routes:</h2>{html_list}"

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
