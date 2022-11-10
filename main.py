import httpx
import time
from app.gen_coordinates import get_city_coords
from app.gen_driving_distances import get_driving_distance
from app.read_write_data import read_city_file, write_coordinates, read_coordinates, write_distance_matrix
import asyncio
sem = asyncio.Semaphore(4)


def run_coordinates():
    cities_names = read_city_file()
    cities_coordinates = {"cities": []}

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


async def insert_distance(client: httpx.AsyncClient(), i, j, city_1, city_2, city_1_name, city_2_name, distance_matrix):
    async with sem:
        print(f" combinaison : {i} --- {j} ")

        if i < j:
            distance = await get_driving_distance(
                client=client, city_coordinate_1=city_1.get("coordinates"), city_coordinate_2=city_2.get("coordinates"))
        elif i > j:
            distance = None
        else:
            distance = 0
        if sem.locked():
            print("Concurrency limit reached, waiting ...")
            await asyncio.sleep(1)
        distance_matrix[city_1_name][city_2_name] = distance


async def run_driving_distances():
    tasks = []
    distance_matrix = {}
    cities: list[dict] = read_coordinates()
    async with httpx.AsyncClient() as client:
        for i, city_1 in enumerate(cities):
            city_1_name = city_1.get("city")
            distance_matrix[city_1_name] = {}
            start = time.time()
            for j, city_2 in enumerate(cities):
                city_2_name = city_2.get("city")
                tasks.append(insert_distance(client=client, i=i, j=j,
                                             city_1=city_1, city_2=city_2, city_1_name=city_1_name, city_2_name=city_2_name, distance_matrix=distance_matrix))
        await asyncio.gather(*tasks)
    write_distance_matrix(distance_matrix=distance_matrix)


if __name__ == "__main__":
    # uncomment to get cities coordinates
    # run_coordinates()

    asyncio.run(run_driving_distances())
