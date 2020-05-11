import os

from flask import Flask, render_template, session, request, flash, redirect, url_for, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit, join_room, leave_room

from helpers import login_required
from collections import deque
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

users = []
users_id = {}
created_channels = []
messages = dict()

# 404 error handler
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
    

@app.route("/")
@login_required
def index():
    username = session['username']
    return render_template("index.html", channels=created_channels, username=username, users=users)


@app.route("/signin", methods=['GET','POST'])
def signin():
    session.clear()

    username = request.form.get("username")

    if request.method == "POST":
        # check if user already exists
        if username in users:
            flash("Username already exists.", "danger")
            return render_template("error.html")

        # add users to array
        users.append(username)

        # user is now logged in
        session['username'] = username

        # remember user even if browser is closed
        session.permanent = True
        return redirect( url_for('index') )
    
    else:
        return render_template("signin.html")


@app.route("/help")
def help():
    return render_template("help.html")


@app.route("/logout", methods=['GET'])
def logout():
    try:
        users.remove(session['username'])
    except ValueError:
        pass

    session.clear()
    return redirect( url_for('index') )


@app.route("/create_channel", methods=['GET','POST'])
def create_channel():
    username = session['username']
    new_channel = request.form.get("channel")

    if request.method == "POST":
        if new_channel in created_channels:
            flash("This channel already exists!", "danger")
            return render_template("error.html")

        created_channels.append(new_channel)
        messages[new_channel] = deque()
        return redirect("/channels/" + new_channel)

    else:
        return render_template("create_channel.html", channels=created_channels, username=username, users=users)


@app.route("/channels/<channel>", methods=['GET', 'POST'])
@login_required
def channels(channel):
    username = session['username']
    session['current_channel'] = channel
    
    if request.method == "POST":
        return redirect( url_for('index') )
    else: 
        return render_template("channels.html", channels=created_channels, messages=messages[channel], username=username, users=users)


@app.route("/message/<user>", methods=['GET', 'POST'])
@login_required
def message(user):
    username = session.get('username')
    session['recipient'] = user

    if request.method == "POST":
        return redirect( url_for('index') )
    else:
        return render_template("message.html", channels=created_channels, username=username, users=users)


@socketio.on("joined", namespace='/')
def joined():
    room = session.get('current_channel')

    join_room(room)
    
    emit('status', {
            'user': session.get('username'),
            'channel': room,
            'msg': session.get('username') + ' joined the channel'
        }, room = room )

@socketio.on("left", namespace='/')
def left():
    room = session.get('current_channel')

    leave_room(room)

    emit('status', {
            'msg': session.get('username') + ' left the channel'
        }, room = room )


@socketio.on('send message')
def send_msg(msg, timestamp):
    room = session.get('current_channel')

    if len(messages[room]) > 100:
        messages[room].popleft()

    messages[room].append([timestamp, session.get('username'), msg])

    emit('show message', {
            'user': session.get('username'),
            'timestamp': timestamp,
            'msg': msg
        }, room = room ) 


@socketio.on('username', namespace='/alert')
def receieve_username(username):
    users_id[username] = request.sid
    print(username)
    print(users_id) 


@socketio.on('alert_message', namespace='/alert')
def alert_message(payload):
    recipient_session_id = users_id[payload['username']]
    message = payload['message']
    emit('new_alert_message', message, room = recipient_session_id)
    print(users_id[payload['username']]) 
    print(payload['username'], recipient_session_id) 
    print(message) 

