import os
import telnetlib
from flask import Flask, send_from_directory, jsonify
from jsonp_decorator import support_jsonp
from pyVent import VentriloServer
from SourceQuery import SourceQuery

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

def check_vent(address, port=3784):
    try:
        vent = VentriloServer((address, port))
        vent.updateStatus()
        return vent.getStatus()
    except:
        return None

def check_css(address, port=27015):
    try:
        css = SourceQuery(address, port)
        return css.info()
    except:
        return None

@app.route('/')
def index():
    return send_from_directory("pages", "index.html", mimetype="text/html")

@app.route('/cssstatus')
def cssstatus():
    return send_from_directory("pages", "cssstatus.html", mimetype="text/html")

@app.route('/cssstatus/json')
@support_jsonp
def cssstatus_json():
    response = check_css("css.gilgi.org")
    if response:
        response['status'] = 'online'
        return jsonify(response)
    return jsonify({'status': 'offline'})

@app.route('/cssstatus/html', methods=['GET'])
def cssstatus_html():
    if check_css("css.gilgi.org"):
        return send_from_directory("pages", "online.html", mimetype="text/html")
    return send_from_directory("pages", "offline.html", mimetype="text/html")

@app.route('/ventstatus')
def ventstatus():
    return send_from_directory("pages", "ventstatus.html", mimetype="text/html")

@app.route('/ventstatus/json')
@support_jsonp
def ventstatus_json():
    response = check_vent("vent.gilgi.org")
    if response:
        response['status'] = 'online'
        return jsonify(response)
    return jsonify({'status': 'offline'})

@app.route('/ventstatus/html', methods=['GET'])
def ventstatus_html():
    if check_vent("vent.gilgi.org"):
        return send_from_directory("pages", "online.html", mimetype="text/html")
    return send_from_directory("pages", "offline.html", mimetype="text/html")

@app.route('/tsstatus')
def tsstatus():
    return send_from_directory("pages", "tsstatus.html", mimetype="text/html")

@app.route('/tsstatus/json', methods=['GET'])
@support_jsonp
def tsstatus_json():
    if telnet('ts.gilgi.org'):
        return jsonify({'status': 'online'})
    return jsonify({'status': 'offline'})

@app.route('/tsstatus/html', methods=['GET'])
def tsstatus_html():
    if telnet('ts.gilgi.org'):
        return send_from_directory("pages", "online.html", mimetype="text/html")
    return send_from_directory("pages", "offline.html", mimetype="text/html")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
