from flask import  request, session


online_players={}
def register_socket_events(socketio):

    @socketio.on("connect")
    def handle_connect():

        # retriving the username of the player from the  session
        username= session.get("username")

        if not  username:
            print("No username found on the socket connection")
            return 

        socket_id= request.sid # storing the  socket id of the ocnnection

        online_players[username]= socket_id

        print(f"Player connected: {username}")
        print(f"Socket ID: {socket_id}")
        print("Online players:", online_players)





        print(f"{username} connected to server")

    @socketio.on("disconnect")
    def handle_disconnect():

        username= session.get("username")

        if username and username in online_players:
            del online_players[username]

        print(f"{username} disconnected from server")
        print(f"Online players: {online_players}")