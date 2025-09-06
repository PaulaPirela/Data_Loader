import time
from concurrent.futures import ProcessPoolExecutor
import requests
import os
import csv
import typing as t
import psutil

# --- Auxiliary Functions ---
def read_pokemons(csv_paths: t.List[str]) -> t.Generator[t.Dict[str, str], None, None]:
    for csv_path in csv_paths:
        if os.path.exists(csv_path):
            with open(csv_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    pokemon_name = row.get('Pokemon', '').lower()
                    type_name = row.get('Type1', '').lower()
                    sprite_url = row.get('Sprite', '').strip()
                    if all([pokemon_name, type_name, sprite_url]):
                        yield {'Pokemon': pokemon_name, 'Type1': type_name, 'Sprite': sprite_url}
        else:
            print(f"ADVERTENCIA: No se encontró el archivo {csv_path}. Omitiendo.")

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
        print(f"Descargado: {pokemon_name}.png en '{folder_name}'")
    else:
        print(f"Omitido: {pokemon_name}.png ya existe.")

# --- Main Function ---
def main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
    start_time = time.time()
    psutil.cpu_percent(interval=None)
    
    pokemons_to_download = list(read_pokemons(inputs))
    
    if not pokemons_to_download:
        return {'method': 'Multiprocessing', 'duration': 0.0, 'cpu_percent': 0.0, 'error': 'No se encontraron Pokémon para descargar.'}
        
    tasks_with_args = [(output_dir, data) for data in pokemons_to_download]
    max_workers_processes = os.cpu_count()
    
    with ProcessPoolExecutor(max_workers=max_workers_processes) as executor:
        executor.map(download_image, tasks_with_args)
        
    end_time = time.time()
    cpu_usage = psutil.cpu_percent(interval=1)
    duration = end_time - start_time
    
    return {'method': 'Multiprocessing', 'duration': duration, 'cpu_percent': cpu_usage}








# import time
# import os
# import csv
# import typing as t
# from concurrent.futures import ProcessPoolExecutor
# import requests
# import psutil


# CSV_FOLDER = "C:/Users/paula/Downloads/concurrent-downloads-master/concurrent-downloads-master/data"
# OUTPUT_FOLDER = "output_Multiprocessing"


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
#     Descarga imágenes de Pokémon usando procesamiento en paralelo.
#     Retorna estadísticas de ejecución.
#     """
#     start = time.time()
#     psutil.cpu_percent(interval=None)  # reset cpu usage stats

#     pokemons = list(read_pokemons(inputs))
#     tasks = [(output_dir, p) for p in pokemons]

#     with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
#         list(executor.map(download_image, tasks))

#     end = time.time()
#     return {
#         "method": "Multiprocessing",
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

