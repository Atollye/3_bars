#!/usr/bin/env python
# /home/atollye/current/programming_exercises/3_bars/bars.py



import os, sys, json, re, pprint
from geopy import distance
import math

DEFAULT_PATH = os.path.join(os.path.dirname
                                  (os.path.abspath(__file__)), "bars.json")



def get_path_from_user():
    message_1 = """\nПоскольку вы не указали путь к файлу с данными, будет использован путь по умолчанию: {} " \n"""
    try:
        pth = sys.argv[1]
    except IndexError:
        pth = DEFAULT_PATH
        print(message_1.format(pth))
    return(pth)

def get_location_from_user():
    print("""\nВведите координаты интересующего вас места в градусах в формате десятичной с точностью 6 знаков после точки. \n Пример:\n Введите широту: 55.752805\n Введите долготу: 37.622635\n\n""")

    while True:
        lon = input("Введите долготу:")
        lat = input("Введите широту: ")
        try:
            lat = float(input("Введите долготу"))
            lon = float(input("Введите широту"))
        except ValueError:
            print("Вы ввели данные, которые не являются координатами")
            continue
        coords =  check_latitide_coord(lat), check_longitude_coord(lon)
        if all(coords):
            break
    return coords


def check_latitide_coord(lat):
    # широта от −90° до +90°,
    coord_regex = re.compile(r"(-)?\d\d[\.\,]\d\d\d\d\d\d")
    if re.match(coord_regex, lat) and -90 <=math.trunc(lat) <=90:
        lat = re.match(coord_regex, lat)
    else:
        lat = None
        try:
            lat = float(input("Введите долготу"))
            lon = float(input("Введите широту"))
        except ValueError:
            print("Вы ввели данные, которые не являются координатами")
            continue

def check_longitude_coord(longt):
    #долгота от −180° до +180°
    coord_regex = re.compile(r"(-)?\d\d(\d)?[\.\,]\d\d\d\d\d\d")
    if re.match(coord_regex, longt) and -90 <=math.trunc(lat) <=90:
        lon = re.match(coord_regex, longt)
    else:
        longt = None


def load_data(filepath):
    #обернуть исключениями
    with open(filepath, "r") as file:
        raw_json = json.load(file)
    data = list(raw_json["features"])

    for bar in data:
        bar_name = bar["properties"]["Attributes"]["Name"]
        latitude = bar["geometry"]["coordinates"][1]
        longitude = bar["geometry"]["coordinates"][0]
        seats_count = bar["properties"]["Attributes"]["SeatsCount"]
        bars.append([bar_name, latitude, longitude, seats_count])

#bars = [[bar_name, longitude, latitude, seats_count], [], []]
    return bars


def get_biggest_bar(data):
    bars_dct = dict(zip(bar_names, bar_sizes))
    biggest= filter(lambda key: bars_dct[key] ==
                                 min(bars_dct.values()), bars_dct)
    print(""" "%s" (%s seats) \n""" % (bar, seats_count))



def get_smallest_bar(data):
    bars_dct = dict(zip(bar_names, bar_sizes))
    smallest= filter(lambda key: bars_dct[key] ==
                                 min(bars_dct.values()), bars_dct)
    print(""" "%s" (%s seats) \n""" % (bar, seats_count))


def get_closest_bar(data, longitude, latitude):
#    distances = {"bar_name": distance, "bar_name": distance,}
    for bar in bars:
        bar_coords = bar[1], bar[2]
        distance_to_bar = distance.distance(user_coords, bar_coords).km
        bar.append(distance_to_bar)

    nearest_bar = min(bars, key=lambda x: x[4])
    print(""" "%s" (%s seats) \n""" % (bar, seats_count))


if __name__ == '__main__':
    print(check_latitide_coord())

