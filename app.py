from flask import Flask, request, redirect, render_template, url_for
from flask_socketio import SocketIO

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
