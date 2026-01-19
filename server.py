from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='..', static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

viewers = 0

@app.route('/')
def index():
    return send_from_directory('index.html')

@socketio.on('connect')
def handle_connect():
    global viewers
    viewers += 1
    emit('viewer_count', viewers, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global viewers
    viewers -= 1
    emit('viewer_count', viewers, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
