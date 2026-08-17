import os
from flask import Flask
from flask_socketio import SocketIO
from game.socket_events import register_socket_events


from dotenv import load_dotenv
# loading the envrionment variables from the root folder.
load_dotenv()

# Import your blueprint object from routes.py
from routes.route import main_bp



app = Flask(__name__)

# global  configuration for the secret key
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


# Global Configuration for storage

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# Initialize Socket.IO
socketio = SocketIO() # creating the socket.io server object
socketio.init_app(app)

'''
socket.io server is resposnsible for doing things such as:
1. knowing registered  events like connect, disconnect, search_player etc..
2. manage the  client connections
3. sending and  brodcasting  the events
4.  managing the  rooms

'''

# Registering the main blueprint here
app.register_blueprint(main_bp)


#registering the same socket.io server instance to the event handler as  well
register_socket_events(socketio)

if __name__ == "__main__":
    # Start the Flask app using the Socket.IO server,
    # so both HTTP routes and Socket.IO events are supported.
    socketio.run(app, debug=True) 
