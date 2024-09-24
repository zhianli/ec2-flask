import socket
import time
from flask import Flask, request, make_response, g, abort, url_for, render_template, redirect

app = Flask(__name__)

server_ip = socket.gethostbyname(socket.gethostname())

@app.before_request
def set_global_value():
    g.client_ip = request.remote_addr
    g.client_port = request.environ.get('REMOTE_PORT')
    g.protocol = request.environ.get('SERVER_PROTOCOL')
    g.routes = sorted([
        rule.rule.lstrip('/') for rule in app.url_map.iter_rules()
        if 'GET' in rule.methods
        and rule.endpoint != 'static'
        and rule.rule != '/' # Exclude the root route
        and not rule.rule.startswith('/process/') # Exclude the /process/<int:status_code> route
    ])

@app.context_processor
def inject_routes():
    return dict(routes=g.routes)

@app.route('/')
def index():
    return redirect('/homepage')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/ip_info')
def ip_addresses():
    ip_info = {
        "client_ip": g.client_ip,
        "client_port": g.client_port,
        "server_ip": server_ip,
        "protocol": g.protocol
    }
    return render_template('ip_info.html', ip_addresses=ip_info)

@app.route('/headers')
def headers():
    headers = []
    for header in sorted(request.headers.keys()):
        headers.append(f'{header}: {request.headers.get(header)}')
    # return '<br>'.join(headers)
    return render_template('headers.html', headers=headers)

@app.route('/status')
def status():
    return render_template('status.html')

@app.route('/process/<int:status_code>')
def return_status(status_code):
    if status_code < 200 or status_code >= 600:
        abort(404)
    return f"Status code: {status_code}", status_code

@app.route('/add_delay', methods=['GET', 'POST'])
def add_delay():
    if request.method == 'POST':
        try:
            delay = int(request.form['delay'])
            if delay > 0:
                time.sleep(delay)
                return render_template('delay_finished.html', delay=delay)
        except ValueError:
            pass

    return render_template('add_delay.html')

# @app.route('/generate_numbers', methods=['GET'])
# def generate_numbers():
#     return render_template('random_numbers.html')

# @app.route('/badminton')
# def badminton():
#     return render_template('badminton.html')

if __name__ == "__main__":
    app.run(host=server_ip, port=80, debug=True)
