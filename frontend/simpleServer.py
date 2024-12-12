from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from flask_cors import CORS  # Import CORS to handle cross-origin requests

app = Flask(__name__)

# Enable CORS for all routes (allow frontend to make requests to the backend)
CORS(app)

# Mocked database of users
users_db = {
    "admin": {
        "password" : "123456",
        "roles": ["admin"],
        "introduction": "I am a super administrator",
        "avatar": "https://media1.tenor.com/m/VPW95GiH_BwAAAAC/blue-archive-ni-ga.gif",
        "name": "supervisor",
        "realname" : "XUXINYU",
        "id" : "3310022004040400030"
    }
}


@app.route('/vue-admin-template/user/logout', methods=['POST'])
def logout():
    response = {
            "code": 20000,
            "data": "success"
        }
    return jsonify(response), 200


@app.route('/vue-admin-template/user/register', methods=['POST'])
def register():
    data = request.get_json()
    print(data)
    response = {
            "code": 20000,
            "data": "success"
        }
    return jsonify(response), 200


@app.route('/vue-admin-template/user/chat', methods=['POST'])
def chatting():
    data = request.get_json()
    print(data)
    response = {
            "code": 20000,
            "text": "消息已收到！正在处理中" 
        }
    return jsonify(response), 200



@app.route('/vue-admin-template/user/info', methods=['POST'])
def save_user_info():
    print('hello')
    data = request.get_json()
    print(data)
    response = {
            "code": 20000,
            "data": "success"
        }
    return jsonify(response), 200

@app.route('/vue-admin-template/user/info', methods=['GET'])
def get_user_info():
    # Extract the token from the query parameter
    token = request.args.get('token')

    if token == "admin-token":  # Check if the token matches the expected one
        # If the token is valid, return the user data
        user = users_db.get("admin")  # Assuming we have only one user, 'admin'
        
        response = {
            "code": 20000,
            "data": {
                "roles": user['roles'],
                "introduction": user['introduction'],
                "avatar": user['avatar'],
                "name": user['name'],
                "rname": user['realname'],
                'id': user['id']
            }
        }
        return jsonify(response), 200
    else:
        # If the token is invalid, return an error
        response = {
            "code": 40000,
            "message": "Invalid token"
        }
        return jsonify(response), 400

@app.route('/vue-admin-template/user/login', methods=['POST'])
def login():
    # Extract data from the POST request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists in the mocked database
    user = users_db.get(username)

    if user:
        # If credentials are correct, return the user data
        response = {
        	"code":20000,
        	"data": {
        		"token":"admin-token"
        	}
        }
        return jsonify(response), 200
    else:
        # If credentials are incorrect, return an error
        response = {
            "code": 40000,
            "message": "Invalid username or password"
        }
        return jsonify(response), 400

if __name__ == '__main__':
    # Run the app on port 9001 (or any port you choose)
    app.run(debug=True, host="0.0.0.0", port=9006)

