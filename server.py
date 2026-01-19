from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import threading
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode="threading")

viewers = 0
lock = threading.Lock()

@app.route('/Assets/<path:path>')
def send_asset(path):
    return send_from_directory('Assets', path)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

def broadcast_viewer_count():
    with lock:
        logging.info(f"Broadcasting viewer count: {viewers}")
        socketio.emit('viewer_count', viewers)

@socketio.on('connect')
def handle_connect():
    global viewers
    with lock:
        viewers += 1
        logging.info("Client connected, viewers: %s", viewers)
    broadcast_viewer_count()

@socketio.on('disconnect')
def handle_disconnect():
    global viewers
    with lock:
        viewers -= 1
        if viewers < 0:
            viewers = 0
        logging.info("Client disconnected, viewers: %s", viewers)
    broadcast_viewer_count()

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=8000, debug=True)
