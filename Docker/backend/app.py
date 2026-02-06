from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() or request.form.to_dict()
    # Basic processing (extend as needed)
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    print('Received form:', data)
    return jsonify({'status': 'success', 'name': name, 'email': email, 'message': message})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
