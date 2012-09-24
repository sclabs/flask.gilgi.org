import os
import telnetlib
from flask import Flask, send_from_directory

app = Flask(__name__)

def telnet(address, port=10011, timeout=2):
    try:
        connection = telnetlib.Telnet(address, port, timeout)
        output = connection.read_until('TS3', timeout)
        if not output.endswith('TS3'):
            return False
        return True
    except:
        return False

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/tsstatus/script', methods=['GET'])
def tsstatus():
    if telnet('ts.gilgi.org'):
        return send_from_directory("static", "tsonline.js", mimetype="text/javascript")
    return send_from_directory("static", "tsoffline.js", mimetype="text/javascript")

@app.route('/tsstatus/title', methods=['GET'])
def tsstatus():
    if telnet('ts.gilgi.org'):
        return send_from_directory("static", "tsonline.html", mimetype="text/html")
    return send_from_directory("static", "tsoffline.html", mimetype="text/html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
