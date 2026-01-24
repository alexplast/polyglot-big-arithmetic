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
    'Assembler': '#2c3e50', # Dark Blue
    'C':         '#34495e', # Blue Grey
    'C++':       '#0055ff', # Blue
    'Rust':      '#dea584', # Rust color
    'Go':        '#00add8', # Cyan
    'Java':      '#b07219', # Brown/Orange
    'JavaScript':'#f1e05a', # Yellow
    'Fortran':   '#734f96', # Purple
    'Python':    '#3572A5', # Python Blue
}

def load_data(filename):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        print(f"[WARN] {filename} not found, skipping plot.")
        return []
    
    data = []
    with open(path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def save_plot(filename):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, filename)
    plt.savefig(path, bbox_inches='tight', dpi=150)
    print(f"[SUCCESS] Saved chart to {path}")
    plt.close()

def plot_bar(title, languages, times, filename, y_label="Time (ms)", log_scale=False):
    plt.figure(figsize=(10, 6))
    
    # Sort data
    paired = sorted(zip(languages, times), key=lambda x: x[1])
    langs = [p[0] for p in paired]
    vals = [p[1] for p in paired]
    
    # Colors
    bars_colors = [COLORS.get(l, '#95a5a6') for l in langs]
    
    bars = plt.bar(langs, vals, color=bars_colors, zorder=3)
    
    plt.title(title, fontsize=14, pad=20)
    plt.ylabel(y_label, fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)
    
    if log_scale:
        plt.yscale('log')
        plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        label = f"{height:.1f}"
        if height > 1000:
             label = f"{height/1000:.2f}s"
             
        y_pos = height
        if log_scale:
            y_pos = height * 1.1
        else:
            y_pos = height + (max(vals)*0.01)

        plt.text(bar.get_x() + bar.get_width()/2., y_pos,
                 label,
                 ha='center', va='bottom', fontsize=9, rotation=0)

    save_plot(filename)

def run_plotting():
    # 1. BigInt
    data = load_data("bigint_benchmark.csv")
    if data:
        langs = [d['Language'] for d in data]
        # Parse floats
        times = [float(d['Factorial Time (ms)']) for d in data]
        plot_bar("BigInt Factorial (Lower is Better)", langs, times, "bigint_factorial.png")

    # 2. Float
    data = load_data("float_benchmark.csv")
    if data:
        langs = [d['Language'] for d in data]
        times = [float(d['Float Time (ms)']) for d in data]
        # Use log scale because Python is usually way slower
        plot_bar("Float Throughput (Lower is Better)", langs, times, "float_throughput.png", log_scale=True)

    # 3. Matrix
    data = load_data("matrix_benchmark.csv")
    if data:
        langs = [d['Language'] for d in data]
        times = [float(d['Matrix Time (ms)']) for d in data]
        plot_bar("Matrix Multiplication (Lower is Better)", langs, times, "matrix_mult.png", log_scale=True)

    # 4. Sort
    data = load_data("sort_benchmark.csv")
    if data:
        langs = [d['Language'] for d in data]
        times = [float(d['Sort Time (ms)']) for d in data]
        plot_bar("Bubble Sort (Lower is Better)", langs, times, "bubble_sort.png", log_scale=True)

if __name__ == "__main__":
    run_plotting()
