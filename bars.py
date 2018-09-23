#!/usr/bin/env python
# /home/atollye/current/programming_exercises/3_bars/bars.py
import os, json, re, pprint
from geopy import distance

PATH_TO_JSON_FILE = os.path.join(
                      os.path.dirname(os.path.abspath(__file__)), "bars.json")
USER_LOCATION = (55.8008475, 37.7751393)


def get_path_from_user():
    message_1 = """ Введите путь к файлу с данными по барам или нажмите Enter,
    чтобы использовать путь по умолчанию
    """
    inpt = input(message_1)
    if inpt is correct:
        pth = inpt
    return inpt

def get_location_from_user():
    message_2 = \
    """Введите координаты интересующего вас места в формате "широта, долгота" 
    в градусах, с точностью 6 знаков после запятой\n
    Пример:   55.752805, 37.622635   """
    inpt = input(message)
    lat, lon = inpt.trim().split()
    coord_regex = "" ""
    if not re.match(coord_regex, lat) and re.match(coord_regex, lon):
        print("Данные введены в неверном формате")


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
    get_path_from_user()
    get_location_from_user()
    load_data(filepath)
    get_biggest_bar(data)
    get_smallest_bar(data)
    get_closest_bar(data, longitude, latitude)
