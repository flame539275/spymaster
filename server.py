import flask
import json
import os
import pymongo
import random


WORD_COUNT = 25
FIRST_COUNT = 9
SECOND_COUNT = 8
ASSASSIN_COUNT = 1


app = flask.Flask(__name__, static_url_path='', static_folder='public')
client = pymongo.MongoClient()
db = client.test_database
db.games.create_index('game_id', expireAfterSeconds=24*60*60) # ttl = 24 hours
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
    game = db.games.find_one({'game_id': game_id})

    if game is None:
        return flask.jsonify({'msg': 'Invalid game ID'}), 404

    db.games.find_one_and_update({'game_id': game_id},
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
    game_id = flask.request.get_json()['game_id']
    if game_id != '' and not db.games.find_one({'game_id': game_id}) is None:
        return flask.jsonify({
            'error': 'Game with given game_id already exists.'
        }), 400

    game = _create_new_game(game_id)
    db.games.insert_one(game)
    return flask.jsonify({
        'game_id': game['game_id'],
        'spymaster_code': game['spymaster_code'],
    }), 200


@app.route('/game/<game_id>/<code>', methods=['GET'])
@app.route('/game/<game_id>', defaults={'code': None}, methods=['GET'])
def join_game(game_id, code):
    game = db.games.find_one({'game_id': game_id})

    if game is None:
        return flask.jsonify({'msg': 'Invalid game ID or Code'}), 404

    return flask.jsonify(_return_game_data(game, code)), 200


def _return_game_data(game, code=None):
    guessed = set(game['guessed'])
    blueGuessed = guessed.intersection(set(game['blue']))
    redGuessed = guessed.intersection(set(game['red']))
    blueScore = len(game['blue']) - len(blueGuessed)
    redScore = len(game['red']) - len(redGuessed)

    if str(game['spymaster_code']) == str(code):
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


def _create_new_game(game_id=''):
    game = _create_game()
    if game_id == '':
        game_id = _create_game_id()
    spymaster_code = _generate_spymaster_code()
    game['game_id'] = game_id
    game['spymaster_code'] = spymaster_code
    return game


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

    return {
        'assassin': assassin,
        'neutral': neutral,
        'blue': first if first_label else second,
        'red': second if first_label else first,
        'tiles': tiles,
        'guessed': [],
    }


def _create_game_id():
    games = db.games.find({})
    names = { game['game_id'] for game in games }
    eligible = words - names
    return random.sample(eligible, 1)[0]


def _generate_spymaster_code():
    return random.sample(words, 1)[0]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))
