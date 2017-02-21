import Webparser
import json
import time
import random
from datetime import datetime

player_details = {'x-player-token': '', 'Content-Type': 'application/json', 'User-agent': 'okhttp/3.4.1'}
gotchi_file = "gotchi_details.json"
bar_objects = ['food', 'attention', 'knowledge']


def load_gotchi_details():
    """ For loading gotchi credentials like x-player-token from file """
    try:
        return json.loads(open(gotchi_file).read())['user-token']
    except:
        return None


def get_score(json_data):
    """Method for getting score out of string"""
    try:
        json_conv = json.loads(json_data)
        if 'game' in json_conv:
            if 'score' in json_conv['game']:
                return json.loads(json_data)['game']['score']
    except:
        pass
    return "error"


def get_care_left(json_data):
    """Method for checking if there is any care left in the server"""
    try:
        return json.loads(json_data)['game']['careLeft']
    except:
        return 10

def get_care_reset(json_data):
    """Method for getting date when carecounter is reset, until this is done no updates can be made.
        Returns current date when could not parse date from string (midnight)"""
    date = datetime.now()
    try:
        time_data = json.loads(json_data)['game']['careReset'].split('T')[1].replace("Z", "").split('.')[0].split(':')
        return date.replace(hour=int(time_data[0])+1, minute=int(time_data[1]), second=int(time_data[2]))
    except:
        return date


if __name__ == '__main__':
    player_key = load_gotchi_details()
    if player_key is None:
        print("player details could net be loaded!")
    else:
        player_details['x-player-token'] = player_key
        print("loaded user details: " + player_key)

        while True:
            request = Webparser.get('https://api.kamergotchi.nl/game', player_details)
            cure_reset = get_care_reset(request)
            if cure_reset > datetime.now() and get_care_left(request) == 0:
                wait_time = (cure_reset-datetime.now()).seconds
                if wait_time > 600:
                    wait_time = 600
                print("waiting " + str(wait_time) + " seconds before continuing")
                time.sleep(wait_time)

            bar_change = bar_objects[random.randint(0, len(bar_objects)-1)]
            post_data = Webparser.post('https://api.kamergotchi.nl/game/care',
                                       json.dumps({'bar': bar_change}), player_details)
            print("added " + bar_change + " to score --> " + str(get_score(post_data)))
