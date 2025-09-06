# analytics.py
import pandas as pd
import matplotlib.pyplot as plt
from benchmark import runners, get_csv_files

CSV_FOLDER = "C:/Users/paula/Downloads/concurrent-downloads-master/concurrent-downloads-master/data"
OUTPUT_FOLDER = "output"


def collect_metrics() -> pd.DataFrame:
    csv_files = get_csv_files(CSV_FOLDER)
    results = runners(OUTPUT_FOLDER, csv_files)
    return pd.DataFrame(results)




def descriptive_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza analítica descriptiva comparando métodos.
    """
    numeric_cols = [c for c in ["duration", "cpu_percent"] if c in df.columns]
    summary = df[numeric_cols].describe().T

    # Ranking solo para los que tengan datos
    if "duration" in df.columns:
        df["rank_duration"] = df["duration"].rank()
    if "cpu_percent" in df.columns:
        df["rank_cpu"] = df["cpu_percent"].rank()

    return summary


def plot_comparison(df: pd.DataFrame) -> None:
    """
    Muestra gráficos comparativos de duración y uso de CPU.
    """
    if "method" not in df.columns:
        raise ValueError("El DataFrame no contiene la columna 'method'.")

    valid = df.dropna(subset=["duration", "cpu_percent"])

    # Duración
    valid.plot(x="method", y="duration", kind="bar", legend=False)
    plt.ylabel("Duración (segundos)")
    plt.title("Comparación de Duración por Método")
    plt.show()

    # CPU
    valid.plot(x="method", y="cpu_percent", kind="bar", legend=False, color="orange")
    plt.ylabel("Uso de CPU (%)")
    plt.title("Comparación de Uso de CPU por Método")
    plt.show()