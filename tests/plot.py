#!/usr/bin/env python3
import os
import csv
import sys

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    print("[ERROR] matplotlib not found. Please run: pip install matplotlib")
    sys.exit(0)

RESULTS_DIR = "results"
PLOTS_DIR = os.path.join(RESULTS_DIR, "plots")

COLORS = {
    'Assembler': '#2c3e50', 'C': '#555555', 'C++': '#00599C',
    'Rust': '#dea584', 'Go': '#00add8', 'Java': '#b07219',
    'JavaScript':'#f1e05a', 'Fortran': '#734f96', 'Python': '#3572A5',
}

def load_data(filename):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path): return []
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader: data.append(row)
    return data

def save_plot(filename):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, filename)
    # Use bbox_inches='tight' instead of tight_layout to handle labels safely
    plt.savefig(path, dpi=100, bbox_inches='tight')
    print(f"Generated plot: {path}")
    plt.close()

def plot_horizontal(title, languages, times, filename, x_label="Time (ms)", log_scale=False):
    plt.figure(figsize=(10, 6))
    
    paired = sorted(zip(languages, times), key=lambda x: x[1], reverse=True)
    langs = [p[0] for p in paired]
    vals = [p[1] for p in paired]
    colors = [COLORS.get(l, '#999999') for l in langs]
    
    bars = plt.barh(langs, vals, color=colors, height=0.6, zorder=3)
    
    plt.title(title, fontsize=14, pad=15)
    plt.xlabel(x_label, fontsize=11)
    plt.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    
    if log_scale:
        plt.xscale('log')
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
        plt.gca().xaxis.set_minor_formatter(ticker.NullFormatter())

    for bar in bars:
        width = bar.get_width()
        x_pos = width * 1.05 if log_scale else width + (max(vals) * 0.01)
        plt.text(x_pos, bar.get_y() + bar.get_height()/2, 
                 f"{width:.1f} ms", va='center', fontsize=9, fontweight='bold')

    if not log_scale: plt.xlim(0, max(vals) * 1.15)
    else: plt.xlim(right=max(vals) * 3)

    save_plot(filename)

def run_plotting():
    data = load_data("bigint_benchmark.csv")
    if data:
        plot_horizontal("BigInt: Factorial Calc (Lower is Better)", 
                        [d['Language'] for d in data], 
                        [float(d['Factorial Time (ms)']) for d in data], "bigint.png")

    data = load_data("float_benchmark.csv")
    if data:
        key = [k for k in data[0].keys() if 'Float Time' in k][0]
        plot_horizontal("Float Math Throughput (Lower is Better)", 
                        [d['Language'] for d in data], 
                        [float(d[key]) for d in data], "float.png")

    data = load_data("matrix_benchmark.csv")
    if data:
        key = [k for k in data[0].keys() if 'Time' in k][0]
        plot_horizontal("Matrix Multiplication (Lower is Better)", 
                        [d['Language'] for d in data], 
                        [float(d[key]) for d in data], "matrix.png", log_scale=True)

    data = load_data("sort_benchmark.csv")
    if data:
        key = [k for k in data[0].keys() if 'Time' in k][0]
        plot_horizontal("Bubble Sort (Lower is Better)", 
                        [d['Language'] for d in data], 
                        [float(d[key]) for d in data], "sort.png", log_scale=True)

if __name__ == "__main__":
    run_plotting()
