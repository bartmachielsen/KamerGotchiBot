import Webparser
import json
import time
import random
from datetime import datetime

playerdetails = {'x-player-token': 'android:d3638728cc6d68b6', 'Content-Type': 'application/json', 'User-agent': 'okhttp/3.4.1'}

bar_objects = ['food', 'attention', 'knowledge']


def get_score(json_data):
    return json.loads(json_data)['game']['score']

def get_care_left(json_data):
    return json.loads(json_data)['game']['careLeft']

def get_care_reset(json_data):
    date = datetime.now()
    splitted = json.loads(json_data)['game']['careReset'].split('T')[1].replace("Z", "").split('.')[0].split(':')
    return date.replace(hour=int(splitted[0])+1, minute=int(splitted[1]), second=int(splitted[2]))


while True:
    request = Webparser.get('https://api.kamergotchi.nl/game', playerdetails)
    cure_reset = get_care_reset(request)
    if cure_reset > datetime.now() and get_care_left(request) == 0:
        wait_time = (cure_reset-datetime.now()).seconds
        print("SLEEPING FOR " + str(wait_time))
        time.sleep(wait_time)

    print(get_score(Webparser.post('https://api.kamergotchi.nl/game/care',
                                   json.dumps({'bar': bar_objects[random.randint(0, len(bar_objects)-1)]}), playerdetails)))
