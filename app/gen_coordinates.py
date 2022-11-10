'''
File: gen_coordinates.py
File Created: Thursday, 10th November 2022 11:32:39 am
Author: KHALIL HADJI 
-----
Copyright:  HENCEFORTH 2022
'''
import httpx
API_KEY = "3958bf8f98a744c79f9d852f8052ebd4"
BASE_URL_COORDINATES_API = "https://api.opencagedata.com/geocode/v1/json?q={city_name}%2C%20{country_name}&key={API_KEY}&pretty=1"


def get_city_coords(client: httpx.Client, city_name: str, country_name: str = "Morocco") -> dict:
    response = client.get(BASE_URL_COORDINATES_API.format(
        city_name=city_name, country_name=country_name, API_KEY=API_KEY))
    if response.status_code == 403:
        return {"country": country_name, "city": city_name, "coordinates": None}
    return {"country": country_name, "city": city_name, "coordinates": response.json()['results'][0]['geometry']}
