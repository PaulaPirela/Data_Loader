# benchmark.py
import os
from multiprocessing_ import main as run_multiprocessing
from threading_ import main as run_threading
from asyncio_ import main as run_asyncio

# 🔑 Constantes globales que deben estar disponibles para analytics.py
CSV_FOLDER = "C:/Users/paula/Downloads/concurrent-downloads-master/concurrent-downloads-master/data"
OUTPUT_FOLDER = "output"

def get_csv_files(folder: str) -> list[str]:
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".csv")
    ]


def normalize_result(result: dict | None, method_name: str) -> dict:
    if not result or not isinstance(result, dict):
        return {
            "method": method_name,
            "duration": None,
            "cpu_percent": None,
            "status": "failed",
        }
    return {
        "method": result.get("method", method_name),
        "duration": result.get("duration"),
        "cpu_percent": result.get("cpu_percent"),
        "status": "ok",
    }


def runners(output: str, inputs: list[str]) -> list[dict]:
    results = []
    results.append(normalize_result(run_multiprocessing(output, inputs), "Multiprocessing"))
    results.append(normalize_result(run_threading(output, inputs), "Threading"))
    results.append(normalize_result(run_asyncio(output, inputs), "Asyncio"))
    return results
