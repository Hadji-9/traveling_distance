'''
File: gen_driving_distances.py
File Created: Thursday, 10th November 2022 11:33:50 am
Author: KHALIL HADJI 
-----
Copyright:  HENCEFORTH 2022
'''
import httpx
BASE_URL_DRIVING_DISTANCE_API = "http://router.project-osrm.org/route/v1/driving/{longitude_1},{latitude_1};{longitude_2},{latitude_2}?overview=false"
cities_coordinates = {"cities": []}


async def get_driving_distance(client: httpx.AsyncClient, city_coordinate_1: dict, city_coordinate_2: dict):
    longitude_1 = city_coordinate_1.get("lng")
    latitude_1 = city_coordinate_1.get("lat")
    longitude_2 = city_coordinate_2.get("lng")
    latitude_2 = city_coordinate_2.get("lat")

    response = await client.get(BASE_URL_DRIVING_DISTANCE_API.format(
        longitude_1=longitude_1, latitude_1=latitude_1, longitude_2=longitude_2, latitude_2=latitude_2))
    return float(response.json()["routes"][0]["distance"])/1000


def get_driving_distance_sync(client: httpx.Client, city_coordinate_1: dict, city_coordinate_2: dict):
    longitude_1 = city_coordinate_1.get("lng")
    latitude_1 = city_coordinate_1.get("lat")
    longitude_2 = city_coordinate_2.get("lng")
    latitude_2 = city_coordinate_2.get("lat")

    response = client.get(BASE_URL_DRIVING_DISTANCE_API.format(
        longitude_1=longitude_1, latitude_1=latitude_1, longitude_2=longitude_2, latitude_2=latitude_2))
    return float(response.json()["routes"][0]["distance"])/1000
