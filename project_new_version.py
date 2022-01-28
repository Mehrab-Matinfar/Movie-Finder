import flask as flask
from flask import Response
from flask import request
from flask import Flask
import json
import requests
import os

url = "https://api.telegram.org/bot5030500889:AAH3DqPa8XE5woVZwKbJrFpWXRWHz_5gnNw/"
url_imdb = "https://imdb8.p.rapidapi.com/auto-complete"
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
            sendMessage(chat_id, "Hi, Welcome to Movie Finder!")
            sendMessage(chat_id, '/list_of_favorit_movies')
            sendMessage(chat_id, '/search_new_movie')
        elif text == '/search_new_movie':
            sendMessage(chat_id, 'Enter the name of movie')

            querystring = {'q': text}
            headers = {
                'x-rapidapi-host': "imdb8.p.rapidapi.com",
                'x-rapidapi-key': "cfd0364257msh4cc69ee1095c46ap16ede2jsn87149799a7da"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            sendMessage(chat_id, response.json())

        elif text == '/list_of_favorit_movies':
            favorit_movies = read_json()
            username = msg['message']['from']['username']
            if username not in favorit_movies.keys():
                sendMessage(chat_id, 'No movie has been selected so far')
            else:
                for movie in favorit_movies[username]:
                    sendMessage(chat_id, movie)

        return Response('ok', status=200)


def write_json(data, filename='favorite_movies.json'):
    with open(filename, 'w') as target:
        json.dump(data, target, indent=4, ensure_ascii=False)


def read_json(filename="favorite_movies.json"):
    with open(filename, 'r') as target:
        data = json.load(target)
    return data



try:
    read_json()
except:
    write_json({})
app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))