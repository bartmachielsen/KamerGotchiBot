import requests

def post(address, content, params):
    return requests.post(address, data=content, headers=params).text

def get(address, params):
    return requests.get(address, headers=params).text