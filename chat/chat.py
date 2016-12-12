from flask import Flask, session, render_template, request, jsonify, abort
from flask_socketio import SocketIO, emit
import requests
import os

app = Flask(__name__)
app.secret_key = app.secret_key = os.urandom(32)
app.debug = False
app.config['REST_API_URL'] = 'http://localhost:5000'

sck_io = SocketIO(app, async_mode="threading")


@app.route('/<string:room>', methods=['GET'])
def home(room):
    if room in ['favicon.ico', 'login']:
        abort(400)
    email = session.get('email', '')
    if email == '':
        return render_template('login.html')
    else:
        return render_template('chat.html', room=room, user=email)


@app.route('/<string:room>', methods=['POST'])
def login(room):
    email = request.form.get('email', '')
    if not email == '':
        session['email'] = email
    else:
        return home(room)
    return render_template('chat.html', room=room, user=session['email'])


@app.route('/new_message/', methods=['POST'])
def post_message():
    if request.json:
        requests.post(app.config.get('REST_API_URL') + '/api', json=request.json)
        return jsonify(result=True), 201
    else:
        abort(400)


@app.route('/<string:room>/get_messages/', methods=['GET'])
def retrieve_messages_from_room(room):
    if room in ['favicon.ico', 'login']:
        abort(400)
    response = requests.get(app.config.get('REST_API_URL') + '/api/' + room)
    data = response.json().get('history', "")
    if data == "":
        return jsonify({'result': []}), 200
    return jsonify({'result': data}), 200


@sck_io.on('new_message', namespace='/alert')
def notify_all_users(message):
    emit('update_list', {'data': message['data']}, broadcast=True)

if __name__ == '__main__':
    sck_io.run(app=app, port=8000)
