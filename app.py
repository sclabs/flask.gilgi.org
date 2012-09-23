import os
import PyTS3
from flask import Flask, send_from_directory
from timeout import timeout

app = Flask(__name__)

@timeout(2, False)
def isOnline(address, port=10011):
    server = PyTS3.ServerQuery(address, port)
    try:
        status = server.connect()
        return status
    except:
        return False

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/tsstatus', methods=['GET'])
def tsstatus():
    if isOnline('ts.gilgi.org'):
        return send_from_directory("static", "tsonline.js", mimetype="text/javascript")
    return send_from_directory("static", "tsoffline.js", mimetype="text/javascript")

@app.route('/awsstatus', methods=['GET'])
def awsstatus():
    if isOnline('aws.gilgi.org'):
        return send_from_directory("static", "awsonline.js", mimetype="text/javascript")
    return send_from_directory("static", "awsoffline.js", mimetype="text/javascript")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
