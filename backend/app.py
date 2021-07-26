import random

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ITEMS = []
APP_DETAILS = {}
REWIEWS = {}


def _pre_init():
    global ITEMS
    data = requests.get('http://api.steampowered.com/ISteamApps/GetAppList/v2/?format=json').json()
    ITEMS = data['applist']['apps']


def _load_app_details(appid):
    global ITEMS
    if appid in APP_DETAILS.keys():
        return APP_DETAILS[appid]
    data = requests.get('http://store.steampowered.com/api/appdetails?appids=' + str(appid)).json()
    item = data[str(appid)]['data']
    APP_DETAILS[appid] = item
    return item


def _load_reviews(appid):
    global ITEMS
    if appid in REWIEWS.keys():
        return REWIEWS[appid]
    data = requests.get('http://store.steampowered.com/appreviews/' + str(appid) + '?json=1&language=russian').json()
    items = data['reviews']
    REWIEWS[appid] = items
    return items


def _gen_items():
    items = []
    while len(items) < 3:
        try:
            appid = random.choice(ITEMS)['appid']
            item = _load_app_details(appid)
            if item['type'] != 'game':
                continue
            items.append(item)
        except Exception as e:
            print('get item error:', e)
    return items


@app.route("/new-round")
@cross_origin()
def new_round():
    if len(ITEMS) <= 3:
        return "Round start error", 404

    items = _gen_items()

    review = None
    counter = 0
    while review is None:
        if counter == 3:
            items = _gen_items()
            counter = 0
            continue
        try:
            reviews = _load_reviews(random.choice(items)['steam_appid'])
            review = random.choice(reviews)
        except Exception as e:
            print('get reviews error:', e)
            counter += 1

    return jsonify({
        'items': list(
            map(lambda x: {'appid': x['steam_appid'], 'name': x['name'], 'image_url': x['header_image']}, items)),
        'review': {
            'id': review['recommendationid'],
            'body': review['review'],
            'play_time': review['author']['playtime_at_review'],
            'recommended': review['voted_up']
        }
    })


@app.route("/check-answer")
@cross_origin()
def check_answer():
    appid = request.args.get('appid')
    if not appid and not appid.isdigit():
        return "'appid' is invalid", 400

    recommendationid = request.args.get('id')
    if not recommendationid and not recommendationid.isdigit():
        return "'id' is invalid", 400

    reviews = REWIEWS.get(int(appid))
    if not reviews:
        return jsonify({'answer': False})
    ids = list(map(lambda x: x['recommendationid'], reviews))
    if recommendationid in ids:
        return jsonify({'answer': True})
    else:
        return jsonify({'answer': False})


if __name__ == '__main__':
    _pre_init()
    app.run(port=5001)
