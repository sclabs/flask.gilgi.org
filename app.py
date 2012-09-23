import os
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/tsstatus', methods=['GET'])
def tsstatus():
    return send_from_directory("static", "tsoffline.js", mimetype="text/javascript")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
