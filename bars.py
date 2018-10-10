#!/usr/bin/env python
# /home/atollye/current/programming_exercises/3_bars/bars.py

import os
import sys
import re
import json
import pprint
from geopy import distance

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                 "bars.json")
USER_LOCATION = (55.646354, 37.719613)

def get_path_to_data_file():
    message_1 = "\nПоскольку вы не указали путь к файлу с данными при"+ \
    " запуске скрипта, будет\nиспользован путь по умолчанию:\n{}\n"
    try:
        pth = sys.argv[1]
    except IndexError:
        pth = DEFAULT_PATH
        print(message_1.format(pth))
    return(pth)

def load_data(filepath):
    try:
        with open(filepath, "r") as file: 
            file_obj = json.load(file)
    except json.JSONDecodeError:
        file_obj = None
    return file_obj

def check_data_structure(json_file):
    try:
        bar = json_file["features"][11]
        bar_name = bar["properties"]["Attributes"]["Name"]
        latitude = bar["geometry"]["coordinates"][1]
        longitude = bar["geometry"]["coordinates"][0]
        seats_count = bar["properties"]["Attributes"]["SeatsCount"]
        address = bar["properties"]["Attributes"]["Address"]
        phone = bar["properties"]["Attributes"]["PublicPhone"]
        correct = True
    except (KeyError, TypeError):
        correct = False
    return correct

def get_coordinates_from_user():
    print("\nВведите координаты интересующего вас места (в градусах "+ 
        "в формате десятичной \nдроби с точностью 6 знаков после точки)."+ 
        " \n\nПример:\nШирота 55.752805\nДолгота 37.622635\n\n")
    inpt = input("Введите широту:  ")
    lat = check_latitude(inpt)
    lon = None
    if lat:
        inpt = input("Введите долготу:  ")
        lon = check_longitude(inpt)
    coords = lat, lon
    return coords

def check_latitude(inpt):
    inpt = inpt.replace(",", ".")
    # 4 знака после запятой дают приемлимую точность определения координаты  
    # на яндекс.каратах, 3 знака -- уже большое отклонение (около 70 метров):
    lat_regex = re.compile(r"(-)?\d\d\.\d\d\d\d(\d)?(\d)?(\d)?")
    match = re.search(lat_regex, inpt)
    if match:
        lat = float(match.group())
    else:
        lat = None
    # широта должна быть от −90° до +90°,
    if lat and (lat <=-90 or lat>=90):
        lat = None
    return lat

def check_longitude(inpt):
    inpt = inpt.replace(",", ".")
    lon_regex = re.compile(r"(-)?\d\d(\d)?\.\d\d\d\d(\d)?(\d)?(\d)?")
    match = re.search(lon_regex, inpt)
    if match:
        lon = float(match.group())
    else:
        lon = None
    #долгота должна быть от −180° до +180°
    if lon and (lon <=-180 or lon>=180):
        lon = None
    return lon

"""
    bar_name = bar["properties"]["Attributes"]["Name"]
    latitude = bar["geometry"]["coordinates"][1]
    longitude = bar["geometry"]["coordinates"][0]
    seats_count = bar["properties"]["Attributes"]["SeatsCount"]
"""

def get_biggest_bar(bars_dct):
    seats_lst = [bar["properties"]["Attributes"]["SeatsCount"] for
                                                           bar in bars_dct]
    max_seats = max(seats_lst)
    biggest= filter(lambda x: x["properties"]["Attributes"]["SeatsCount"] == 
    max_seats, bars_dct)

    #pprint.pprint(list(biggest))
    return biggest


def get_smallest_bar(bars_dct):
    seats_lst = [bar["properties"]["Attributes"]["SeatsCount"] for
                                                           bar in bars_dct]
    min_seats = min(seats_lst)
    smallest= filter(lambda x: x["properties"]["Attributes"]["SeatsCount"] == 
    min_seats, bars_dct)

    pprint.pprint(list(smallest))
    return smallest


def get_nearest_bar(user_coords, data):
    nearest = min(bars, key=lambda x: distance.distance(user_coords, 
             (x["geometry"]["coordinates"][1], 
              x["geometry"]["coordinates"][0])).km)
    pprint.pprint(nearest)
    return nearest


"""
Описание функции min-max
https://younglinux.info/python/feature/min-max
Известные алгоритмы на Python
https://younglinux.info/algorithm
"""

# def printout(results_list):
#     pass
#     #     print(""" "%s" (%s seats) \n""" % (bar, seats_count))

def error_exit(message=""):
    print(message)
    print("Попробуйте перезапустить скрипт и ввести данные заново")
    sys.exit()

def main():
    path_to_data = get_path_to_data_file()
    if not os.path.exists(path_to_data):
        error_exit("Файл с данными не существует")
    file_obj = load_data(path_to_data)
    if not file_obj:
        error_exit("Данные в файле не соответствуют формату json")
    if not check_data_structure(file_obj):
        error_exit("Данный json файл не содержит данные о барах" + 
            " в требуемом программой формате")
    
    bars = file_obj["features"]
    pprint.pprint(get_biggest_bar(bars))

    # pprint.pprint(bars)
    # printout((get_biggest_bar(bars)))
    # printout(get_smallest_bar(bars))

    # coordinates = get_coordinates_from_user()
    # if not coordinates[0]:
    #     error_exit("\nВы ввели несуществующую широту\n")
    # elif not coordinates[1]:
    #     error_exit(("\nВы ввели несуществующую долготу\n"))
    
    # printout(get_nearest_bar(coordinates, bars_json))



if __name__ == '__main__':
    file_obj = load_data(DEFAULT_PATH)
    bars = file_obj["features"]
    get_nearest_bar(USER_LOCATION, bars)








