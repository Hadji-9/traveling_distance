import httpx
import time
from app.gen_coordinates import get_city_coords
from app.gen_driving_distances import get_driving_distance
from app.read_write_data import read_city_file, write_coordinates, read_coordinates, write_distance_matrix
import typer
cities_coordinates = {"cities": []}
# app = typer.Typer()


def run_coordinates():
    cities_names = read_city_file()

    result = []
    start = time.time()
    with httpx.Client() as client:
        total = len(cities_names)
        for i, city in enumerate(cities_names):
            time.sleep(1.1)
            coords = get_city_coords(
                client=client, city_name=city)
            if coords.get("coordinates"):
                result.append(coords)
            else:
                result.append(coords)
                break
            print(f'-------- {i} out of {total} --------')

    cities_coordinates["cities"] = result
    cities_coordinates["duration"] = f"{time.time()-start} seconds"
    write_coordinates(coordinates=cities_coordinates)


def run_driving_distances():
    distance_matrix = {}
    cities: list[dict] = read_coordinates()
    with httpx.Client() as client:
        for i, city_1 in enumerate(cities):
            city_1_name = city_1.get("city")
            distance_matrix[city_1_name] = {}
            for j, city_2 in enumerate(cities):
                city_2_name = city_2.get("city")

                if i < j:
                    distance = get_driving_distance(
                        client=client, city_coordinate_1=city_1.get("coordinates"), city_coordinate_2=city_2.get("coordinates"))
                elif i > j:
                    distance = None
                else:
                    distance = 0

                distance_matrix[city_1_name][city_2_name] = distance
    write_distance_matrix(distance_matrix=distance_matrix)


if __name__ == "__main__":
    run_driving_distances()
    # app()
