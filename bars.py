import json
from math import sin, cos, asin, sqrt, radians
import sys


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        return json.loads(json_file.read())['features']


def get_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_coordinates(bar):
    return map(radians, bar['geometry']['coordinates'])


def get_distance(bar, latitude, longitude):
    # Use haversine formula
    # https://en.wikipedia.org/wiki/Haversine_formula
    earth_radius = 6372.8
    latitude_of_bar, longitude_of_bar = get_coordinates(bar)
    d_of_lat = (latitude_of_bar - latitude) / 2
    d_of_lon = (longitude_of_bar - longitude) / 2
    mult_of_cos = cos(latitude_of_bar) * cos(latitude)
    sphere_distance = sin(d_of_lat) ** 2 + mult_of_cos * sin(d_of_lon) ** 2
    return 2 * asin(sqrt(sphere_distance)) * earth_radius


def get_biggest_bar(bars_list):
    biggest_bar = max(bars_list, key=get_seats_count)
    return biggest_bar


def get_smallest_bar(bars_list):
    smallest_bar = min(bars_list, key=get_seats_count)
    return smallest_bar


def get_closest_bar(bars_list, latitude, longitude):
    closest_bar = min(
        bars_list,
        key=lambda bar: get_distance(bar, latitude, longitude)
    )
    return closest_bar


if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.exit('No file')
    file_path = sys.argv[1]
    bars = load_data(file_path)
    try:
        longitude = radians(float(input('Enter longitude: ')))
        latitude = radians(float(input('Enter latitude: ')))
    except ValueError:
        sys.exit('Координаты введены неверно.')
    print(
        'Самый большой бар:',
        get_biggest_bar(bars)['properties']['Attributes']['Name']
    )
    print(
        'Самый маленький бар:',
        get_smallest_bar(bars)['properties']['Attributes']['Name']
    )
    closest_bar = get_closest_bar(bars, latitude, longitude)
    print(
        'Ближайший бар:',
        closest_bar['properties']['Attributes']['Name']
    )
