import time
from concurrent.futures import ThreadPoolExecutor
import requests
import os
import csv
import typing as t
import psutil

def read_pokemons(csv_paths: t.List[str]) -> t.Generator[t.Dict[str, str], None, None]:
    for csv_path in csv_paths:
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                pokemon_name = row.get('Pokemon', '').lower()
                type_name = row.get('Type1', '').lower()
                sprite_url = row.get('Sprite', '').strip()
                if all([pokemon_name, type_name, sprite_url]):
                    yield {'Pokemon': pokemon_name, 'Type1': type_name, 'Sprite': sprite_url}

def download_image(args: t.Tuple[str, t.Dict[str, str]]):
    output_dir, pokemon_data = args
    pokemon_name = pokemon_data['Pokemon']
    folder_name = pokemon_data['Type1']
    image_url = pokemon_data['Sprite']
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    image_path = os.path.join(folder_path, f"{pokemon_name}.png")
    if not os.path.exists(image_path):
        response = requests.get(image_url, timeout=15)
        response.raise_for_status()
        with open(image_path, 'wb') as f:
            f.write(response.content)

def main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
    try:
        start_time = time.time()
        psutil.cpu_percent(interval=None)
        pokemons_to_download = list(read_pokemons(inputs))
        tasks_with_args = [(output_dir, data) for data in pokemons_to_download]
        max_workers_threads = min(32, os.cpu_count() + 4)
        with ThreadPoolExecutor(max_workers=max_workers_threads) as executor:
            list(executor.map(download_image, tasks_with_args))
        end_time = time.time()
        cpu_usage = psutil.cpu_percent(interval=1)
        duration = end_time - start_time
        return {'method': 'Threading', 'duration': duration, 'cpu_percent': cpu_usage}
    except Exception as e:
        print(f"Error en el método de Threading: {e}")
        return {'method': 'Threading', 'duration': 0.0, 'cpu_percent': 0.0}



















# import time
# import os
# import csv
# import typing as t
# from concurrent.futures import ThreadPoolExecutor
# import requests
# import psutil


# CSV_FOLDER = "C:/Users/paula/Downloads/concurrent-downloads-master/concurrent-downloads-master/data"
# OUTPUT_FOLDER = "output_threading"


# def read_pokemons(csv_paths: t.List[str]) -> t.Generator[t.Dict[str, str], None, None]:
#     """
#     Lee múltiples archivos CSV y produce diccionarios con la información de cada Pokémon.
#     Filtra aquellos que tengan nombre, tipo y URL de sprite válidos.
#     """
#     for path in csv_paths:
#         with open(path, mode="r", encoding="utf-8-sig") as f:
#             for row in csv.DictReader(f):
#                 pokemon = row.get("Pokemon", "").strip().lower()
#                 type1 = row.get("Type1", "").strip().lower()
#                 sprite = row.get("Sprite", "").strip()

#                 if pokemon and type1 and sprite:
#                     yield {"Pokemon": pokemon, "Type1": type1, "Sprite": sprite}


# def download_image(args: t.Tuple[str, t.Dict[str, str]]) -> None:
#     """
#     Descarga la imagen de un Pokémon en la carpeta correspondiente a su tipo.
#     Si la imagen ya existe, no se descarga nuevamente.
#     """
#     output_dir, pokemon = args
#     name, type1, url = pokemon["Pokemon"], pokemon["Type1"], pokemon["Sprite"]

#     folder = os.path.join(output_dir, type1)
#     os.makedirs(folder, exist_ok=True)

#     path = os.path.join(folder, f"{name}.png")
#     if not os.path.exists(path):
#         response = requests.get(url, timeout=15)
#         response.raise_for_status()
#         with open(path, "wb") as f:
#             f.write(response.content)


# def main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
#     """
#     Descarga imágenes de Pokémon usando hilos (threading).
#     Retorna estadísticas de ejecución.
#     """
#     start = time.time()
#     psutil.cpu_percent(interval=None)  # reset cpu usage stats

#     pokemons = list(read_pokemons(inputs))
#     tasks = [(output_dir, p) for p in pokemons]

#     # ThreadPool típico: limitado a 32 o CPUs+4
#     max_workers = min(32, (os.cpu_count() or 1) + 4)
#     with ThreadPoolExecutor(max_workers=max_workers) as executor:
#         list(executor.map(download_image, tasks))

#     end = time.time()
#     return {
#         "method": "Threading",
#         "duration": end - start,
#         "cpu_percent": psutil.cpu_percent(interval=1),
#     }


# if __name__ == "__main__":
#     # Recolectar todos los CSV en la carpeta definida
#     csv_files = [
#         os.path.join(CSV_FOLDER, file)
#         for file in os.listdir(CSV_FOLDER)
#         if file.endswith(".csv")
#     ]

#     stats = main(OUTPUT_FOLDER, csv_files)
#     print("Ejecución terminada:", stats)
