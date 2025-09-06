# asyncio_script.py
import time
import asyncio
import aiohttp
import aiofiles
import os
import csv
import typing as t
import psutil
import nest_asyncio

# 🔑 Parcheamos el loop existente (Jupyter/IPython compatible)
nest_asyncio.apply()


def read_pokemons(csv_paths: t.List[str]) -> t.Generator[t.Dict[str, str], None, None]:
    for csv_path in csv_paths:
        with open(csv_path, mode="r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pokemon_name = row.get("Pokemon", "").lower()
                type_name = row.get("Type1", "").lower()
                sprite_url = row.get("Sprite", "").strip()
                if all([pokemon_name, type_name, sprite_url]):
                    yield {
                        "Pokemon": pokemon_name,
                        "Type1": type_name,
                        "Sprite": sprite_url,
                    }


async def download_image_async(session: aiohttp.ClientSession, output_dir: str, pokemon_data: t.Dict[str, str]):
    pokemon_name = pokemon_data["Pokemon"]
    folder_name = pokemon_data["Type1"]
    image_url = pokemon_data["Sprite"]

    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    image_path = os.path.join(folder_path, f"{pokemon_name}.png")
    if not os.path.exists(image_path):
        async with session.get(image_url, timeout=15) as response:
            response.raise_for_status()
            async with aiofiles.open(image_path, "wb") as f:
                await f.write(await response.read())


async def async_main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
    start_time = time.time()
    psutil.cpu_percent(interval=None)

    pokemons_to_download = list(read_pokemons(inputs))
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, output_dir, data) for data in pokemons_to_download]
        await asyncio.gather(*tasks)

    end_time = time.time()
    cpu_usage = psutil.cpu_percent(interval=1)
    duration = end_time - start_time

    return {"method": "Asyncio", "duration": duration, "cpu_percent": cpu_usage}


def main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
    """
    Ejecuta el flujo asyncio en cualquier entorno (script normal o Jupyter).
    """
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_main(output_dir, inputs))


# import time
# import asyncio
# import aiohttp
# import aiofiles
# import os
# import csv
# import typing as t
# import psutil
# import nest_asyncio


# CSV_FOLDER = "C:/Users/paula/Downloads/concurrent-downloads-master/concurrent-downloads-master/data"
# OUTPUT_FOLDER = "output"


# # Para entornos como Jupyter, evita errores de event loop
# nest_asyncio.apply()


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


# async def download_image_async(
#     session: aiohttp.ClientSession, output_dir: str, pokemon: t.Dict[str, str]
# ) -> None:
#     """
#     Descarga la imagen de un Pokémon usando peticiones asíncronas.
#     Si la imagen ya existe, no se descarga nuevamente.
#     """
#     name, type1, url = pokemon["Pokemon"], pokemon["Type1"], pokemon["Sprite"]

#     folder = os.path.join(output_dir, type1)
#     os.makedirs(folder, exist_ok=True)

#     path = os.path.join(folder, f"{name}.png")
#     if not os.path.exists(path):
#         async with session.get(url, timeout=15) as response:
#             response.raise_for_status()
#             async with aiofiles.open(path, "wb") as f:
#                 await f.write(await response.read())


# async def async_main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
#     """
#     Ejecuta la descarga de imágenes en paralelo usando asyncio.
#     Retorna estadísticas de ejecución.
#     """
#     start = time.time()
#     psutil.cpu_percent(interval=None)  # reset cpu usage stats

#     pokemons = list(read_pokemons(inputs))

#     async with aiohttp.ClientSession() as session:
#         tasks = [download_image_async(session, output_dir, p) for p in pokemons]
#         await asyncio.gather(*tasks)

#     end = time.time()
#     return {
#         "method": "Asyncio",
#         "duration": end - start,
#         "cpu_percent": psutil.cpu_percent(interval=1),
#     }


# def main(output_dir: str, inputs: t.List[str]) -> t.Dict[str, t.Union[str, float]]:
#     """
#     Punto de entrada síncrono para ejecutar el flujo asíncrono.
#     """
#     return asyncio.run(async_main(output_dir, inputs))


# if __name__ == "__main__":
#     # Recolectar todos los CSV en la carpeta definida
#     csv_files = [
#         os.path.join(CSV_FOLDER, file)
#         for file in os.listdir(CSV_FOLDER)
#         if file.endswith(".csv")
#     ]

#     stats = main(OUTPUT_FOLDER, csv_files)
#     print("Ejecución terminada:", stats)
