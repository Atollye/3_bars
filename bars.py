#!/usr/bin/env python
# /home/atollye/current/programming_exercises/3_bars/bars.py

import os
import sys
import re
import json
# import pprint
from geopy import distance

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                 "bars.json")



def get_path_to_data_file():
    message_1 = """\nПоскольку вы не указали путь к файлу с данными при запуске скрипта, будет\nиспользован путь по умолчанию:\n{}\n"""
    try:
        pth = sys.argv[1]
    except IndexError:
        pth = DEFAULT_PATH
        print(message_1.format(pth))
    return(pth)

def load_data(filepath):
    try:
        with open(filepath, "r") as file: 
            raw_json = json.load(file)
            print("File loaded")
    except json.JSONDecodeError:
        print("It's not a json file")
        raw_json = None
    return raw_json


def get_coordinates_from_user():
    print("""\nВведите координаты интересующего вас места (в градусах в формате десятичной \nдроби с точностью 6 знаков после точки). \n\nПример:\nШирота 55.752805\nДолгота 37.622635\n\n""")
    lon = None
    inpt = input("Введите широту:  ")
    lat = check_latitude(inpt)
    if lat:
        inpt = input("Введите долготу:  ")
        lon = check_longitude(inpt)
    else:
        print("\nВы ввели несуществующую широту\n")

    if lat and not lon:
        print("\nВы ввели несуществующую долготу\n")
    coords = lat, lon
    if not all(coords):
        coords = None
    return coords

def check_latitude(inpt):
    inpt = inpt.replace(",", ".")
    # 4 знака после запятой дают приемлимую точность на яндекс.каратах, 3 знака -- уже большое отклонение (около 70 метров)
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


    

def get_biggest_bar(data):
    """
    data_structure
    bar_name = bar["properties"]["Attributes"]["Name"]
    latitude = bar["geometry"]["coordinates"][1]
    longitude = bar["geometry"]["coordinates"][0]
    seats_count = bar["properties"]["Attributes"]["SeatsCount"]
    # извлечь адрес и телефон
    """



    bars_dct = dict(zip(bar_names, bar_sizes))
    biggest= filter(lambda key: bars_dct[key] ==
                                 min(bars_dct.values()), bars_dct)
    print(""" "%s" (%s seats) \n""" % (bar, seats_count))

def get_smallest_bar(data):
    bars_dct = dict(zip(bar_names, bar_sizes))
    smallest= filter(lambda key: bars_dct[key] ==
                                 min(bars_dct.values()), bars_dct)
    print(""" "%s" (%s seats) \n""" % (bar, seats_count))
    
def get_nearest_bar(user_coords, data):
    # distances = {"bar_name1": distance1, "bar_name2": distance2,}
    for bar in bars:
        bar_coords = bar[1], bar[2]
        distance_to_bar = distance.distance(user_coords, bar_coords).km
        bar.append(distance_to_bar)

    nearest_bar = min(bars, key=lambda x: x[4])
    print(""" "%s" (%s seats) \n""" % (bar, seats_count))

def printout(bar_list):
    pass

def error_exit(message=""):
    print(message)
    print("Попробуйте перезапустить скрипт и ввести данные заново")
    sys.exit()

def main():
    path_to_data = get_path_to_data_file()
    if not os.path.exists(path_to_data):
        error_exit("Файл с данными не существует")
    raw_json = load_data(path_to_data)
    if not raw_json:
        error_exit("Данные в файле не соответствуют формату json")
    if not check_data_structure(raw_json):
        error_exit("Данный json файл не содержит данные о барах в требуемом формате. Возможно, он поврежден или получен из другого источника")
    bars = raw_json["features"]

    printout(get_smallest_bar(bars))
    printout((get_biggest_bar(bars)))

    coordinates = get_coordinates_from_user()
    if not coordinates[0]:
        error_exit("\nВы ввели несуществующую широту\n")
    elif not coordinates[1]:
        error_exit(("\nВы ввели несуществующую долготу\n"))
    
    printout(get_nearest_bar(coordinates, bars))








if __name__ == '__main__':

:







