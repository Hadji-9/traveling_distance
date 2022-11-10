import httpx
import time
from app.gen_coordinates import get_city_coords
from app.gen_driving_distances import get_driving_distance
from app.read_write_data import read_city_file, write_coordinates
cities_coordinates = {"cities": [], "duration": ""}


def run_coordinates():
    cities_names = read_city_file()

    result = []
    start = time.time()
    with httpx.Client() as async_client:
        total = len(cities_names)
        for i, city in enumerate(cities_names):
            time.sleep(1.1)
            coords = get_city_coords(
                client=async_client, city_name=city)
            if coords.get("coordinates"):
                result.append(coords)
            else:
                result.append(coords)
                break
            print(f'-------- {i} out of {total} --------')

    cities_coordinates["cities"] = result
    write_coordinates(coordinates=cities_coordinates)
    cities_coordinates["duration"] = f"{time.time()-start} seconds"


if __name__ == "__main__":
    run_coordinates()
