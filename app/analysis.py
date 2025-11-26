import pandas as pd
import json
import os
import matplotlib.pyplot as plt

def compute_statistics(csv_path):
    df = pd.read_csv(csv_path)
    numeric = df.select_dtypes(include="number").copy()

    stats = {
        "rows": int(len(df)),
        "columns": list(df.columns),
        "numeric_columns": list(numeric.columns),
        "mean": numeric.mean().to_dict(),
        "median": numeric.median().to_dict(),
        "variance": numeric.var(ddof=0).to_dict(),
        "std": numeric.std(ddof=0).to_dict(),
        "describe": json.loads(numeric.describe().to_json()),
        "correlation": numeric.corr().to_dict()
    }
    # Save stats to outputs
    os.makedirs("outputs", exist_ok=True)
    json_path = f"outputs/{os.path.basename(csv_path).replace('.csv','')}_stats.json"
    with open(json_path, "w") as f:
        json.dump(stats, f)
    return stats, json_path

def plot_numeric_histogram(csv_path, column, output_filename=None):
    df = pd.read_csv(csv_path)
    if column not in df.columns:
        raise ValueError("Column not found")
    os.makedirs("outputs", exist_ok=True)
    if output_filename is None:
        output_filename = f"outputs/{os.path.basename(csv_path).replace('.csv','')}_{column}_hist.png"
    plt.figure()
    df[column].dropna().hist()
    plt.title(f"Histogram of {column}")
    plt.xlabel(column)
    plt.ylabel("count")
    plt.savefig(output_filename)
    plt.close()
    return output_filename
