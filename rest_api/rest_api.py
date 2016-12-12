from flask import Flask, request, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
app.debug = False
db = MongoClient('mongodb://deguchre:ep11DVvR#Ft$@ds119368.mlab.com:19368/restdb').restdb


def is_valid(data):
    if not type(data) == dict:
        return False
    for field in ['user', 'room', 'message', 'date_time']:
        if field not in data:
            return False
    return True


@app.route('/api', methods=['POST'])
def post():
    if request.json:
        if not request.json.get("message", "") == "":
            message_data = request.json['message']
            if is_valid(message_data):
                messages = db.messages
                messages.insert(message_data)
                return jsonify(result=True), 201
    return abort(400)


@app.route('/api/<string:room>', methods=['GET'])
def get_messages(room):
    messages = db.messages
    history = []
    for data in messages.find({'room': room}, {'_id': False}):
        if is_valid(data):
            history.append(data)
    return jsonify({'history': history}), 200

if __name__ == '__main__':
    app.run()
