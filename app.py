from flask import Flask, jsonify, request
from flask_cors import CORS
from ConncectPLC import Mysocket as sock
import uuid
import re

rule = re.compile("B")
rule1 = re.compile("DM")

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'B03',
        'bool': True,
        'str': False,
        'myvalue' : ""
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'B02',
        'bool': True,
        'str': False,
        'myvalue' : ""
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'B01',
        'bool': True,
        'str': False,
        'myvalue' : ""
    }
]

# configuration
DEBUG = True
socket = sock("192.168.10.10",8501)
# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'bool': post_data.get('bool'),
            'str': False,
            'myvalue' : ""
        })
        response_object['message'] = 'address added!'
    else:
        for Book in BOOKS:
            Booltype = rule.findall(Book['title'])
            if len(Booltype) > 0:
                status = tobool(socket.Get(Book['title']))
                Book['bool'] = status
                Book['str'] = False
                Book['myvalue'] = ""
                print("Bool")
            else:
                strtype = rule1.findall(Book['title'])
                if len(strtype) > 0:
                    status = socket.Get(Book['title'],".U")
                    Book['bool'] = False
                    Book['str'] = True
                    Book['myvalue'] = str(status)

        response_object['books'] = BOOKS
    return jsonify(response_object)

@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        # remove_book(book_id)
        # BOOKS.append({
        #     'id': uuid.uuid4().hex,
        #     'title': post_data.get('title'),
        #     'bool': post_data.get('bool'),
        #     'str' : post_data.get('str'),
        #     'value' : post_data.get('value'),
        # })
        # print(post_data.get('title'))
        Booltype = rule.findall(post_data.get('title'))
        if len(Booltype) > 0:
            socket.Send(post_data.get('title'), tostr(post_data.get('bool')))
            print("bool1111111111111")
        else:
            strtype = rule1.findall(post_data.get('title'))
            if len(strtype) > 0:
                socket.Send(post_data.get('title'), post_data.get('myvalue'),".U")
        
        response_object['message'] = 'addr updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'addr removed!'
    return jsonify(response_object)
    
def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False

def tobool(bool):
        if bool == "1":
            return True
        elif bool == "0":
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
