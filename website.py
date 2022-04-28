from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def index():
    client_ip = request.remote_addr # https://www.adamsmith.haus/python/answers/how-to-get-an-ip-address-using-flask-in-python
    client_port = request.environ.get('REMOTE_PORT') # https://stackoverflow.com/questions/34785337/how-to-use-flask-get-clients-port
    server_ip = request.host.split(':')[0] # https://stackoverflow.com/questions/41024296/how-to-show-my-ip-address-on-flask
    protocol = request.environ.get('SERVER_PROTOCOL')
    return f"<p>client: {client_ip}:{client_port} <br> server ip: {server_ip} <br> protocol: {protocol}</p>"

if __name__ == "__main__":
    app.run(port=80)