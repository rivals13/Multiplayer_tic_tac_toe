def register_socket_events(socketio):

    @socketio.on("connect")
    def handle_connect():
        print("A player connected")

    @socketio.on("disconnect")
    def handle_disconnect():
        print("A player disconnected")