import os
import telnetlib
#from flask import send_from_directory
from flask import jsonify, render_template, make_response, request
from jsonp_decorator import support_jsonp
from pyVent import VentriloServer
from SourceQuery import SourceQuery
import pages
import steamservices
import sc2services
from minecraft_query import MinecraftQuery
import dota2services
import eveservices
from app import app

def online():
    response = make_response(open('app/static/online.html').read())
    response.headers["Content-type"] = "text/html"
    return response

def offline():
    response = make_response(open('app/static/offline.html').read())
    response.headers["Content-type"] = "text/html"
    return response

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

def check_minecraft(address, port=25565, timeout=3):
    try:
        query = MinecraftQuery(address, port, timeout=timeout)
        return query.get_status()
    except:
        return None

@app.route('/')
def index():
    return render_template("index.html", data=pages.index)

@app.route('/sc2')
@support_jsonp
def sc2():
    return jsonify(sc2services.getdata());

@app.route('/dota2')
@support_jsonp
def dota2():
    return jsonify(dota2services.getdata());

@app.route('/steam')
@support_jsonp
def steam():
    return jsonify(steamservices.getdata());

@app.route('/cssstatus')
def cssstatus():
    return render_template("index.html", data=pages.cssstatus)

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
        return online()
        #return send_from_directory("static", "online.html", mimetype="text/html")
    return offline()
    #return send_from_directory("static", "offline.html", mimetype="text/html")

@app.route('/ventstatus')
def ventstatus():
    return render_template("index.html", data=pages.ventstatus)

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
        return online()
        #return send_from_directory("static", "online.html", mimetype="text/html")
    return offline()
    #return send_from_directory("static", "offline.html", mimetype="text/html")

@app.route('/tsstatus')
def tsstatus():
    return render_template("index.html", data=pages.tsstatus)

@app.route('/tsstatus/json', methods=['GET'])
@support_jsonp
def tsstatus_json():
    if telnet('ts.gilgi.org'):
        return jsonify({'status': 'online'})
    return jsonify({'status': 'offline'})

@app.route('/tsstatus/html', methods=['GET'])
def tsstatus_html():
    if telnet('ts.gilgi.org'):
        return online()
        #return send_from_directory("static", "online.html", mimetype="text/html")
    return offline()
    #return send_from_directory("static", "offline.html", mimetype="text/html")

@app.route('/minecraftstatus')
def minecraftstatus():
    return render_template("index.html", data=pages.minecraftstatus)

@app.route('/minecraftstatus/json', methods=['GET'])
@support_jsonp
def minecraftstatus_json():
    response = check_minecraft("minecraft.gilgi.org")
    if response:
        response['status'] = 'online'
        return jsonify(response)
    return jsonify({'status': 'offline'})

@app.route('/minecraftstatus/html', methods=['GET'])
def minecraftstatus_html():
    if check_minecraft("minecraft.gilgi.org"):
        return online()
        #return send_from_directory("static", "online.html", mimetype="text/html")
    return offline()
    #return send_from_directory("static", "offline.html", mimetype="text/html")

@app.route('/eve/balance', methods=['GET'])
@support_jsonp
def eve_balance():
    keyID = request.args.get('keyID')
    vCode = request.args.get('vCode')
    try:
        return jsonify({'balance': eveservices.get_balance(keyID, vCode)})
    except Exception as e:
        return jsonify({'balance': str(e)})

@app.route('/eve/skilltraining', methods=['GET'])
@support_jsonp
def eve_skill_training():
    keyID = request.args.get('keyID')
    vCode = request.args.get('vCode')
    try:
        return jsonify({'skilltraining': eveservices.get_skill_in_training(keyID, vCode)})
    except Exception as e:
        return jsonify({'skilltraining': str(e)})

@app.route('/eve/skillqueue', methods=['GET'])
@support_jsonp
def eve_skill_queue():
    keyID = request.args.get('keyID')
    vCode = request.args.get('vCode')
    try:
        return jsonify({'skillqueue': eveservices.get_skill_queue(keyID, vCode)})
    except Exception as e:
        return jsonify({'skillqueue': [str(e)]})

@app.route('/eve/orders', methods=['GET'])
@support_jsonp
def eve_orders():
    keyID = request.args.get('keyID')
    vCode = request.args.get('vCode')
    try:
        return jsonify({'orders': eveservices.get_orders(keyID, vCode)})
    except Exception as e:
        return jsonify({'orders': [str(e)]})