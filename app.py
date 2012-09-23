import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/tsstatus', methods=['GET'])
def tsstatus():
    response = make_response(open('tsoffline.js').read())
    response.headers["Content-type"] = "text/javascript"
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
