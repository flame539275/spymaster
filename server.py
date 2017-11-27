import bson.json_util
import bson.objectid
import flask
import json
import os
import pymongo
import random
import uuid


WORD_COUNT = 25
FIRST_COUNT = 9
SECOND_COUNT = 8
ASSASSIN_COUNT = 1


app = flask.Flask(__name__, static_url_path='', static_folder='public')
client = pymongo.MongoClient()
db = client.test_database
with open('wordlist.txt', 'r') as fp:
    words = set([line.strip() for line in fp.readlines()])


@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory('public', 'favicon.ico')


@app.route('/')
def home_page():
    return flask.send_from_directory('public', 'index.html')


@app.route('/game')
def game_page():
    return flask.send_from_directory('public', 'game.html')


@app.route('/guess/<game_id>/<code>/<word>', methods=['POST'])
def guess_word(game_id, code, word):
    real_id = bson.objectid.ObjectId(game_id)
    game = db.games.find_one({'_id': real_id})

    if game is None:
        return flask.jsonify({'msg': 'Invalid game ID'}), 404

    db.games.find_one_and_update({'_id': real_id},
        {
            '$push': {
                'guessed': word
            }
        })

    game = _return_game_data(game, code)
    game['guessed'].append(word)
    return flask.jsonify(game), 200


@app.route('/new_game', methods=['POST'])
def new_game():
    game = _create_game()
    game_id = db.games.insert_one(game).inserted_id
    return flask.jsonify({
        'game_id': str(game_id),
        'player_code': game['url_player'],
        'spymaster_code': game['url_spymaster'],
    }), 200


@app.route('/game/<game_id>/<code>', methods=['GET'])
def join_game(game_id, code):
    real_id = bson.objectid.ObjectId(game_id)
    game = db.games.find_one({'_id': real_id})

    if game is None:
        return flask.jsonify({'msg': 'Invalid game ID or Code'}), 404

    if game['url_player'] != code and game['url_spymaster'] != code:
        return flask.jsonify({'msg': 'Invalid game ID or Code'}), 404

    return flask.jsonify(_return_game_data(game, code)), 200


def _return_game_data(game, code):
    guessed = set(game['guessed'])
    blueGuessed = guessed.intersection(set(game['blue']))
    redGuessed = guessed.intersection(set(game['red']))
    blueScore = len(game['blue']) - len(blueGuessed)
    redScore = len(game['red']) - len(redGuessed)

    if game['url_player'] == code:
        return { 'assassin': list(guessed.intersection(set(game['assassin']))),
                 'blue': list(blueGuessed),
                 'guessed': game['guessed'],
                 'isSpymaster': False,
                 'neutral': list(guessed.intersection(set(game['neutral']))),
                 'red': list(redGuessed),
                 'tiles': game['tiles'],
                 'blueScore': blueScore,
                 'redScore': redScore,
               }

    if game['url_spymaster'] == code:
        return { 'assassin': game['assassin'],
                 'blue': game['blue'],
                 'guessed': game['guessed'],
                 'isSpymaster': True,
                 'neutral': game['neutral'],
                 'red': game['red'],
                 'tiles': game['tiles'],
                 'blueScore': blueScore,
                 'redScore': redScore,
               }


def _create_game():
    chosen = random.sample(words, WORD_COUNT)
    # Assassin
    assassin = random.sample(chosen, ASSASSIN_COUNT)
    for word in assassin:
        chosen.remove(word)
    # First
    first = random.sample(chosen, FIRST_COUNT)
    for word in first:
        chosen.remove(word)
    # Second
    second = random.sample(chosen, SECOND_COUNT)
    for word in second:
        chosen.remove(word)
    # Neutral
    neutral = list(chosen)
    # This is much faster than random.choice([True, False])
    # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
    first_label = random.random()
    # Random tile placement
    tiles = assassin + neutral + first + second
    random.shuffle(tiles)
    # Generate urls
    url_player = uuid.uuid4().get_hex()
    url_spymaster = uuid.uuid4().get_hex()

    return {
        'assassin': assassin,
        'neutral': neutral,
        'blue': first if first_label else second,
        'red': second if first_label else first,
        'tiles': tiles,
        'url_player': url_player,
        'url_spymaster': url_spymaster,
        'guessed': [],
    }


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)), debug=True)
