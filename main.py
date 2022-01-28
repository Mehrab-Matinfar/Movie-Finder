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
    list_of_movies = [
        {"name": "breaking bad", "year": 2012, "genre": "crime"}
    ]
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text', '')

        while True:
            if text == '/start':
                sendMessage(chat_id, "Hi, Welcome to Movie Finder!")
                sendMessage(chat_id, '/list_of_favorit_movies')
                sendMessage(chat_id, '/search_new_movie')
                break
            elif text == '/list_of_favorit_movies':
                favorit_movies = read_json()
                username = msg['message']['from']['username']
                if username not in favorit_movies.keys():
                    sendMessage(chat_id, 'No movie has been selected so far')
                    break
                else:
                    for movie in favorit_movies[username]:
                        sendMessage(chat_id, movie)
                        break

            elif text == '/search_new_movie':
                sendMessage(chat_id, '/year')
                sendMessage(chat_id, '/genre')
                break
            elif text == '/year':
                for movie in list_of_movies:
                    if movie["year"] == 2012:  # i don't know what to do!
                        sendMessage(chat_id, movie["name"])
                break
            elif text == '/genre':
                for movie in list_of_movies:
                    if movie["genre"] == "comedy":  # i don't know what to do!
                        sendMessage(chat_id, movie["name"])
                break
            elif text == 'End':
                break
            else:
                querystring = {'q': text}
                headers = {
                    'x-rapidapi-host': "imdb8.p.rapidapi.com",
                    'x-rapidapi-key': "cfd0364257msh4cc69ee1095c46ap16ede2jsn87149799a7da"
                }
                response = requests.request("GET", url_imdb, headers=headers, params=querystring)
                my_json = response.json()
                sendMessage(chat_id, my_json['d'][0]['i']['imageUrl'])
                #requests.post(url + '/sendphoto?chat_id=' + chat_id + '&&photo=' + my_json['d'][0]['i']['imageUrl'] + '&&caption=' + 'massage')
                #requests.post(url + '/sendPhoto?chat_id=' + str(chat_id) + '&&photo=' + my_json['d'][0]['i']['imageUrl'] + '&&caption=' + 'massage')
                sendMessage(chat_id, "rank = " + str(my_json['d'][0]['rank']))
                break
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
