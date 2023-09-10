from flask import Flask, request, jsonify
import jwt  # For JWT token creation
import uuid  # For generating random user IDs

app = Flask(__name__)

# Replace these with your own values in a production environment
client_id = 'your-client-id'
client_secret = 'your-client-secret'
issuer = 'http://localhost:5000'  # The OIDC issuer URL

# This dictionary simulates a user database (for educational purposes)
user_db = {
    'user1': {
        'sub': 'user1',
        'name': 'Alice',
        'email': 'alice@example.com',
        'password': 'password123'
    }
}

# OIDC endpoint for token issuance
@app.route('/token', methods=['POST'])
def issue_token():
    # Parse the incoming request
    data = request.form
    grant_type = data.get('grant_type')
    client_id_received = data.get('client_id')
    client_secret_received = data.get('client_secret')
    username = data.get('username')
    password = data.get('password')

    # Check client credentials
    if (
        client_id_received != client_id or
        client_secret_received != client_secret
    ):
        return jsonify({'error': 'invalid_client'}), 401

    # Authenticate the user (simplified for demonstration)
    if username not in user_db or user_db[username]['password'] != password:
        return jsonify({'error': 'invalid_grant'}), 400

    # Generate an ID token (JWT)
    user_info = user_db[username]
    token_payload = {
        'sub': user_info['sub'],
        'name': user_info['name'],
        'email': user_info['email'],
        'iss': issuer,
        'aud': client_id
    }
    id_token = jwt.encode(token_payload, client_secret, algorithm='HS256')

    # Return the ID token as a JSON response
    return jsonify({'access_token': id_token, 'token_type': 'bearer'}), 200

if __name__ == '__main__':
    app.run(debug=True)
