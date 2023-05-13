from socket import socket
import time
from flask import Flask, request, redirect, render_template, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user_dict = {}
user_List = []
client_query = []
chat_message = {}


@app.route('/')
@app.route("/login")
def login():  # put application's code here
    return render_template("index.html")


@app.route("/chat/<username>", methods=["POST", "GET"])
def chat_main(username):
    global user_List
    global user_dict
    user_dict[str(request.remote_addr)] = username
    user_List = user_dict.values()
    emit("update_user", {"online": user_List})
    print(user_dict)


@socketio.on('NewMessage')
def handle_new_message(data):
    global chat_message
    content = data.get('content')
    name = data.get("name")
    now = time.asctime()
    chat_message[str(name) + ":" + now] = str(content)
    emit('NewMessage', {"content": content, "sendName": name, "sendTime": now}, broadcast=True)
    print(chat_message)


@socketio.on('connect')  # 有客户端连接会触发该函数
def on_connect():
    global user_List
    global user_dict
    global client_id
    # 建立连接 sid:连接对象ID
    # client_id = request.sid
    # client_query.append(client_id)
    # emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)
    # #对name_space下的所有客户端发送消息
    print(u'new connection,id=[%s] connected, now have [%s] connections' % (request.remote_addr, len(client_query)))


@socketio.on('disconnect')  # 有客户端断开WebSocket会触发该函数
def on_disconnect():
    global user_List
    global user_dict
    # 连接对象关闭 删除对象ID
    # user_dict.pop(str(request.sid))
    # client_query.remove(request.sid)
    # user_List = user_dict.values()
    print(u'connection id=[%s] exited, now have [%s] connections' % (request.remote_addr, len(client_query)))


if __name__ == '__main__':
    # app.run()
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
