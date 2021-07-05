from flask import Flask, jsonify, request
from flask_cors import CORS
from ConncectPLC import Mysocket as sock
import uuid
import re
import json

rule = re.compile("B")
rule1 = re.compile("DM|W")

# socket = sock("192.168.5.88",8501)
socket = sock("192.168.162.20",8501)
# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

try:
    ADDRS = json.load(open( "data.json"))
    if str(type(ADDRS)) == "<class 'NoneType'>":
        ADDRS = []  
except:
    ADDRS = []

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/addrs', methods=['GET', 'POST'])
def all_addrs():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
            
        ADDRS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'bool': post_data.get('bool'),
            'str': False,
            'myvalue' : "",
            'commit' : post_data.get('commit'),
            'ReadOrWrite':post_data.get('ReadOrWrite')
        })
        response_object['message'] = 'address added!'
    else:
        for Addr in ADDRS:
            Booltype = rule.findall(Addr['title'])
            if len(Booltype) > 0:
                status = tobool(socket.Get(Addr['title']))
                Addr['bool'] = status
                Addr['str'] = False
                Addr['myvalue'] = ""
                # print(Addr['title'])
                # print(socket.Get(Addr['title']))
                # print("--------------")
            else:
                strtype = rule1.findall(Addr['title'])
                if len(strtype) > 0:
                    status = socket.Get(Addr['title'],".D")
                    Addr['bool'] = False
                    Addr['str'] = True
                    Addr['myvalue'] = str(status)

        response_object['addrs'] = ADDRS
    return jsonify(response_object)

@app.route('/addrs/<addr_id>', methods=['PUT', 'DELETE'])
def single_addr(addr_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_addr(addr_id)
        ADDRS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'bool': post_data.get('bool'),
            'str' : post_data.get('str'),
            'value' : post_data.get('value'),
            'commit' : post_data.get('commit'),
            'ReadOrWrite':post_data.get('ReadOrWrite')
        })
        # print(post_data.get('title'))
        Booltype = rule.findall(post_data.get('title'))
        if len(Booltype) > 0:
            socket.Send(post_data.get('title'), tostr(post_data.get('bool')))
            # print("bool1111111111111")
        else:
            strtype = rule1.findall(post_data.get('title'))
            if len(strtype) > 0:
                socket.Send(post_data.get('title'), post_data.get('myvalue'),".U")
        
        response_object['message'] = 'addr updated!'
    if request.method == 'DELETE':
        remove_addr(addr_id)
        response_object['message'] = 'addr removed!'
    return jsonify(response_object)

@app.route('/save', methods=['POST'])
def Save_Setting():
    datas = ADDRS
    file = 'data.json'
    with open(file, 'w') as obj:
        json.dump(datas, obj)
    return "True"

@app.route('/load', methods=['POST'])
def Load_Setting():
    global ADDRS
    try:
        ADDRS = json.load( open( "data.json" ) )
        if str(type(ADDRS)) == "<class 'NoneType'>":
            ADDRS = []  
    except:
        ADDRS = []
    return "True"

@app.route('/change', methods=['POST'])
def change():
    global ADDRS
    post_data = request.get_json()
    print()
    old = post_data.get('moved')['oldIndex']
    new = post_data.get('moved')['newIndex']
    ADDRS[old], ADDRS[new] = ADDRS[new], ADDRS[old]
    return "True"


def remove_addr(addr_id):
    print(ADDRS)
    print(addr_id)
    for addr in ADDRS:
        if addr['id'] == addr_id:
            ADDRS.remove(addr)
            return True
    return False

def tobool(bool):
        if bool == "1" or bool == 1:
            return True
        elif bool == "0" or bool == 0:
            return False
        else:
            return "Error"

def tostr(str):
        print(str)
        if str:
            return "1"
        else:
            return "0"

if __name__ == '__main__':

    app.run()
