from flask import Flask, request

app = Flask(__name__)

@app.route('/callback', methods=['GET'])
def callback():
    authorization_token = request.args.get('code')
    return f"Callback received! Authorization token: {authorization_token}"

if __name__ == '__main__':
    app.run(debug=True, port=8888)