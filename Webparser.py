import requests


def post(address, content, params):
    try:
        return requests.post(address, data=content, headers=params).text
    except:
        return None


def get(address, params):
    try:
        return requests.get(address, headers=params).text
    except:
        return None
