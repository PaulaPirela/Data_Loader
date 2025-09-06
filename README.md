Concurrent Downloads Benchmark

Este proyecto evalúa diferentes enfoques de concurrencia en Python para la descarga masiva de imágenes a partir de datos en CSV.

Métodos implementados

Multiprocessing: procesos en paralelo.

Threading: hilos concurrentes.

Asyncio: asincronía basada en corrutinas.

Estructura

multiprocessing_script.py: implementación con ProcessPoolExecutor.

threading_script.py: implementación con ThreadPoolExecutor.

asyncio_script.py: implementación con aiohttp y asyncio.

benchmark.py: ejecuta los tres métodos y recolecta métricas.

analytics.py: análisis descriptivo y visualización de resultados.

notebooks/: notebooks para análisis y visualización.

Resultados

Multiprocessing no es adecuado para tareas I/O-bound.

Threading ofrece la mejor velocidad.

Asyncio logra un buen balance al reducir el consumo de CPU con tiempos competitivos.

Requisitos

Python 3.9+

Dependencias: requests, aiohttp, aiofiles, psutil, pandas, matplotlib, seaborn

Ejecución

Colocar los CSV en la carpeta definida en benchmark.py.

Ejecutar el benchmark:

python benchmark.py


Analizar resultados:

python analytics.py