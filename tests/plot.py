#!/usr/bin/env python3
import argparse
import csv
import os
import sys

try:
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    print("[ERROR] matplotlib not found. Install it locally or run with --no-plots.")
    sys.exit(1)

COLORS = {
    "Assembler": "#2c3e50",
    "C": "#555555",
    "C++": "#00599C",
    "Rust": "#dea584",
    "Go": "#00add8",
    "Java": "#b07219",
    "JavaScript": "#f1e05a",
    "Fortran": "#734f96",
    "Python": "#3572A5",
}


def load_data(results_dir, filename):
    path = os.path.join(results_dir, filename)
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def save_plot(plots_dir, filename):
    os.makedirs(plots_dir, exist_ok=True)
    path = os.path.join(plots_dir, filename)
    plt.savefig(path, dpi=100, bbox_inches="tight")
    print(f"Generated plot: {path}")
    plt.close()


def plot_horizontal(title, languages, times, plots_dir, filename, x_label="Time (ms)", log_scale=False):
    valid_data = [(language, value) for language, value in zip(languages, times) if value > 0]
    if not valid_data:
        print(f"[WARN] No valid data to plot for {title}")
        return

    paired = sorted(valid_data, key=lambda item: item[1], reverse=True)
    langs = [item[0] for item in paired]
    values = [item[1] for item in paired]
    colors = [COLORS.get(language, "#999999") for language in langs]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(langs, values, color=colors, height=0.6, zorder=3)
    plt.title(title, fontsize=14, pad=15)
    plt.xlabel(x_label, fontsize=11)
    plt.grid(axis="x", linestyle="--", alpha=0.5, zorder=0)

    if log_scale:
        plt.xscale("log")
        plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
        plt.gca().xaxis.set_minor_formatter(ticker.NullFormatter())

    max_value = max(values)
    for bar in bars:
        width = bar.get_width()
        x_pos = width * 1.05 if log_scale else width + (max_value * 0.01)
        plt.text(
            x_pos,
            bar.get_y() + bar.get_height() / 2,
            f"{width:.1f} ms",
            va="center",
            fontsize=9,
            fontweight="bold",
        )

    if not log_scale:
        plt.xlim(0, max_value * 1.15)
    else:
        plt.xlim(right=max_value * 3)

    save_plot(plots_dir, filename)


def run_plotting(results_dir):
    plots_dir = os.path.join(results_dir, "plots")

    data = load_data(results_dir, "bigint_benchmark.csv")
    if data:
        plot_horizontal(
            "BigInt: Factorial Calc (Lower is Better)",
            [row["Language"] for row in data],
            [float(row["Factorial Time (ms)"]) for row in data],
            plots_dir,
            "bigint.png",
        )

    data = load_data(results_dir, "float_benchmark.csv")
    if data:
        key = [column for column in data[0].keys() if "Float Time" in column][0]
        plot_horizontal(
            "Float Math Throughput (Lower is Better)",
            [row["Language"] for row in data],
            [float(row[key]) for row in data],
            plots_dir,
            "float.png",
        )

    data = load_data(results_dir, "matrix_benchmark.csv")
    if data:
        key = [column for column in data[0].keys() if column.endswith("Time (ms)")][0]
        plot_horizontal(
            "Matrix Multiplication (Lower is Better)",
            [row["Language"] for row in data],
            [float(row[key]) for row in data],
            plots_dir,
            "matrix.png",
            log_scale=True,
        )

    data = load_data(results_dir, "sort_benchmark.csv")
    if data:
        key = [column for column in data[0].keys() if column.endswith("Time (ms)")][0]
        plot_horizontal(
            "Bubble Sort (Lower is Better)",
            [row["Language"] for row in data],
            [float(row[key]) for row in data],
            plots_dir,
            "sort.png",
            log_scale=True,
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()
    run_plotting(args.results_dir)


if __name__ == "__main__":
    main()
