'''
File: read_files.py
File Created: Thursday, 10th November 2022 11:35:18 am
Author: KHALIL HADJI 
-----
Copyright:  HENCEFORTH 2022
'''

import json


def read_city_file(file_name: str = "cities.txt") -> list:
    with open("./app/" + file_name, "r") as f:
        cities = f.read().split("\n")
    print("*"*30)
    print(f"JUST READ CITIES LIST FROM : /app/{file_name}")
    print("*"*30)
    return cities


def write_coordinates(coordinates: dict, file_name: str = "coordinates.json") -> None:
    with open("./app/" + file_name, "w") as f:
        coordinates_string = json.dumps(coordinates)
        f.write(coordinates_string)
    print("*"*30)
    print(f"COORDINATE ARE SAVED IN FILE : /app/{file_name}")
    print("*"*30)