import requests

def get_data_from_api():
    response = requests.get('https://ckan2.multimediagdansk.pl/gpsPositions')
    return response.json()['vehicles']