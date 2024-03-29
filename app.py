import time

from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
user_dict = {}
chat_message = {}


@app.route('/')
@app.route("/login")
def login():  # put application's code here
    return render_template("index.html")


@socketio.on('NewMessage')  # 新消息
def handle_new_message(data):
    global chat_message
    content = data.get('content')
    name = data.get("name")
    now = time.asctime()
    chat_message[str(name) + ":" + now] = content.encode("utf-8").decode("utf-8")
    emit('NewMessage', {"content": content, "sendName": name, "sendTime": now}, broadcast=True)


@socketio.on('updateList')  # 更新用户列表
def update_online_list(new_user):
    global user_dict
    name = new_user.get("name")
    new_client = str(request.remote_addr) + ":" + name
    user_dict[new_client] = name
    emit("updateList", user_dict, broadcast=True)
    print(user_dict)


@socketio.on('connect')  # 有客户端连接会触发该函数
def on_connect():
    # #对name_space下的所有客户端发送消息
    print(u'new connection,id=[%s] connected' % request.remote_addr)


@socketio.on('leave')  # 有用户离开会触发该函数
def on_disconnect(data):
    global user_dict
    LeaveName = data.get("name")
    # 连接对象关闭 删除对象ID
    for key in list(user_dict.keys()):
        if user_dict[key] == LeaveName:
            user_dict.pop(key)
            emit("OtherLeave", {"name": LeaveName}, broadcast=True)
        else:
            pass
    print("%s离开,聊天室现存：" % LeaveName)
    print(user_dict)


@socketio.on('disconnect')  # 有客户端断开WebSocket会触发该函数
def on_disconnect():
    print("聊天室现存：")
    print(user_dict)


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
