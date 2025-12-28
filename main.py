import requests

response = requests.get('https://ckan2.multimediagdansk.pl/gpsPositions')

data = response.json()
print(data.keys())

vehicles_data = data['vehicles']
print(type(vehicles_data))

first_vehicle = vehicles_data[0]
print(first_vehicle)

for vehicle in vehicles_data:
    if (vehicle['routeShortName'] == '199' or vehicle['routeShortName'] == '168'):
        number = vehicle['routeShortName']
        delay = vehicle['delay']
        coordinates = {'latitude':vehicle['lat'], 'longitude':vehicle['lon']}
        print(f"Line: {number}, delay: {delay}, coordinates: {coordinates['latitude']}, {coordinates['longitude']}")