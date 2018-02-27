import json
from math import sin, cos, asin, sqrt, radians


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        return json.loads(json_file.read())['features']


def get_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_coordinates(bar):
    return map(radians, bar['geometry']['coordinates'])


def get_distance(bar, latitude, longitude):
    earth_radius = 6372.8
    latitude_of_bar, longitude_of_bar = get_coordinates(bar)
    d_of_lat = (latitude_of_bar - latitude) / 2
    d_of_lon = (longitude_of_bar - longitude) / 2
    mult_of_cos = cos(latitude_of_bar) * cos(latitude)
    sphere_distance = sin(d_of_lat) ** 2 + mult_of_cos * sin(d_of_lon) ** 2
    return 2 * asin(sqrt(sphere_distance)) * earth_radius


def get_biggest_bar(bars_list):
    biggest_bar = max(bars_list, key=get_seats_count)
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(bars_list):
    smallest_bar = min(bars_list, key=get_seats_count)
    return smallest_bar['properties']['Attributes']['Name']


def get_closest_bar(bars_list, latitude, longitude):
    def distance_from_bar(bar):
        return get_distance(bar, latitude, longitude)
    closest_bar = min(bars_list, key=distance_from_bar)
    return closest_bar['properties']['Attributes']['Name']

if __name__ == '__main__':
    try:
        longitude = radians(float(input('Enter longitude: ')))
        latitude = radians(float(input('Enter latitude: ')))
        file_path = 'bars.json'
        bars = load_data(file_path)
        print(get_biggest_bar(bars))
        print(get_smallest_bar(bars))
        print(get_closest_bar(bars, latitude, longitude))
    except FileNotFoundError:
        print('No file')
    except json.decoder.JSONDecodeError:
        print('Troubles with content of json file')
    except IndexError:
        print('You did not write the name of file')
