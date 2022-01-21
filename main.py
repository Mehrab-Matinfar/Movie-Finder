import flask as flask
from flask import Response
from flask import request
from flask import Flask
import json
import requests
import os

url = "https://api.telegram.org/bot5030500889:AAH3DqPa8XE5woVZwKbJrFpWXRWHz_5gnNw/"

app = Flask(__name__)


def get_all_updates():
    response = requests.get(url + 'getUpdates')
    return response.json()


def get_last_update(allUpdates):
    return allUpdates['result'][-1]


def get_chat_id(update):
    return update['message']['chat']['id']


def sendMessage(chat_id, text):
    sendData = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url + 'sendMessage', sendData)
    return response


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')
        if text == '/start':
            sendMessage(chat_id, "Hi, Welcome to Movie Finder")
        #.........


def write_json(data, filename='.............'):
    pass
    #..........


def read_json(filename="?????.json"):
    pass
    #..........


try:
    read_json()
except:
    write_json({})
app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
