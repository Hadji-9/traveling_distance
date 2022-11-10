import httpx
import asyncio
import time
API_KEY = "2d955cbff7974520b8b85006f35b1f85"
BASE_URL_COORDINATES_API = "https://api.opencagedata.com/geocode/v1/json?q={city_name}%2C%20{country_name}&key={API_KEY}&pretty=1"
BASE_URL_DRIVING_DISTANCE_API = "http://router.project-osrm.org/route/v1/driving/{longitude_1},{latitude_1};{longitude_2},{latitude_2}?overview=false"
cities = ["rabat", "casablanca", "tanger", "marrakesh"]


def get_city_coords(client: httpx.Client, city_name: str, country_name: str = "Morocco") -> dict:
    response = client.get(BASE_URL_COORDINATES_API.format(
        city_name=city_name, country_name=country_name, API_KEY=API_KEY))
    return response.json()['results'][0]['geometry']


def get_driving_distance(client: httpx.Client, city_coordinate_1: dict, city_coordinate_2: dict):
    longitude_1 = city_coordinate_1.get("lng")
    latitude_1 = city_coordinate_1.get("lat")
    longitude_2 = city_coordinate_2.get("lng")
    latitude_2 = city_coordinate_2.get("lat")

    response = client.get(BASE_URL_DRIVING_DISTANCE_API.format(
        longitude_1=longitude_1, latitude_1=latitude_1, longitude_2=longitude_2, latitude_2=latitude_2, API_KEY=API_KEY))
    return float(response.json()["routes"][0]["distance"])/1000


if __name__ == "__main__":
    start = time.time()
    with httpx.Client() as client:
        for i,city1 in enumerate(cities):
            for j,city2 in enumerate(cities):
                if i < j :
                    city_coordinate_1 = get_city_coords(
                        client=client, city_name=city1)
                    city_coordinate_2 = get_city_coords(
                        client=client, city_name=city2)
                    print(f" distance between {city1} and {city2} is =======>")
                    print(get_driving_distance(
                        client=client, city_coordinate_1=city_coordinate_1, city_coordinate_2=city_coordinate_2), "km", sep=" ")
    print(f"THIS SCRIPT EXECUTION TOOK  {time.time()-start}")
