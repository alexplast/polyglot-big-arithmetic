#!/usr/bin/env python3
import subprocess
import os
import re
import statistics
import csv
import argparse
import time

# --- Configuration ---
RESULTS_DIR = "results"
REPORT_FILE = "RESULTS.md"

DEFAULTS = {
    "bigint": { "fib": "25000", "fact": "5000", "base": "2", "exp": "20000" },
    "float":  { "count": "1475", "loops": "50000" },
    "matrix": { "size": "200" },
    "sort":   { "size": "3000" }
}

def bin_cmd(folder, name, ext=""):
    return f"./bin/{folder}/{name}_{ext}"

def java_cmd(folder, class_name):
    return f"java -cp bin/{folder} {class_name}"

def py_cmd(script):
    return f"python3 src/python/{script}"

def js_cmd(script):
    return f"node src/js/{script}"

LANGS = {
    "asm":      {"name": "Assembler",  "type": "Native"},
    "c":        {"name": "C",          "type": "Custom Base 10^9"},
    "cpp":      {"name": "C++",        "type": "Custom Base 10^9"},
    "rust":     {"name": "Rust",       "type": "Custom Base 10^9"},
    "go":       {"name": "Go",         "type": "math/big"},
    "java":     {"name": "Java",       "type": "BigInteger"},
    "js":       {"name": "JavaScript", "type": "BigInt"},
    "python":   {"name": "Python",     "type": "Native"},
    "fortran":  {"name": "Fortran",    "type": "Custom Base 10^9"},
}

def parse_time(stdout):
    match = re.search(r"Time: ([0-9\.\-eE]+) ms", stdout)
    if match: return float(match.group(1))
    return None

def run_once(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        if result.returncode != 0:
            if result.returncode == 132: return None # Illegal Instruction
            if result.returncode == 139: return None # Segfault
            if "Error:" in result.stdout or "Error:" in result.stderr: return None
            print(f"\n[ERROR] Command failed: {cmd}")
            return None
        return parse_time(result.stdout)
    except Exception as e:
        print(f"\n[EXCEPTION] Error running {cmd}: {e}")
        return None

def run_benchmark_cmd(cmd, env_vars, runs):
    times = []
    print(f"Running {cmd.split('/')[-1]}...", end=" ", flush=True)
    for _ in range(runs):
        t = run_once(cmd, env_vars)
        if t is not None: times.append(t)
        else:
            print("[SKIP]", end=" ")
            return None
    median = statistics.median(times)
    print(f"OK ({median:.2f} ms)")
    return median

# --- Report Management ---

def init_report():
    """Overwrite the report file with a header."""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("# Polyglot Benchmark Results\n\n")
        f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")

def append_report_section(title, markdown_table, image_filename):
    """Append a section with table and image link to the report AND print to console."""
    # Print to console
    print(f"\n--- {title} Results ---")
    print(markdown_table)
    
    # Write to file
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"## {title}\n\n")
        f.write(markdown_table + "\n\n")
        if image_filename:
            f.write(f"![{title} Graph](results/plots/{image_filename})\n\n")
        f.write("---\n\n")

# --- Benchmarks ---

def run_bigint(runs):
    print(f"\n--- 1. BigInt Benchmark (Median of {runs} runs) ---")
    targets = [
        ("C",          bin_cmd("fibo", "fibonacci", "c"),   bin_cmd("fact", "factorial", "c"),   bin_cmd("power", "power", "c")),
        ("C++",        bin_cmd("fibo", "fibonacci", "cpp"), bin_cmd("fact", "factorial", "cpp"), bin_cmd("power", "power", "cpp")),
        ("Rust",       bin_cmd("fibo", "fibonacci", "rs"),  bin_cmd("fact", "factorial", "rs"),  bin_cmd("power", "power", "rs")),
        ("Go",         bin_cmd("fibo", "fibonacci", "go"),  bin_cmd("fact", "factorial", "go"),  bin_cmd("power", "power", "go")),
        ("Java",       java_cmd("fibo", "Fibonacci"),       java_cmd("fact", "Factorial"),       java_cmd("power", "Power")),
        ("Python",     py_cmd("fibonacci.py"),              py_cmd("factorial.py"),              py_cmd("power.py")),
        ("JavaScript", js_cmd("fibonacci.js"),              js_cmd("factorial.js"),              js_cmd("power.js")),
        ("Fortran",    bin_cmd("fibo", "fibonacci", "f90"), bin_cmd("fact", "factorial", "f90"), bin_cmd("power", "power", "f90")),
    ]
    results = []
    env_fib = {"COUNT": DEFAULTS["bigint"]["fib"]}
    env_fact = {"COUNT": DEFAULTS["bigint"]["fact"]}
    env_pow = {"BASE": DEFAULTS["bigint"]["base"], "EXP": DEFAULTS["bigint"]["exp"]}

    for name, cmd_f, cmd_fa, cmd_p in targets:
        t_f = run_benchmark_cmd(cmd_f, env_fib, runs)
        t_fa = run_benchmark_cmd(cmd_fa, env_fact, runs)
        t_p = run_benchmark_cmd(cmd_p, env_pow, runs)
        b_type = next((v["type"] for k, v in LANGS.items() if v["name"] == name), "Unknown")
        results.append({ "name": name, "fib": t_f, "fact": t_fa, "pow": t_p, "type": b_type })

    results.sort(key=lambda x: x['fact'] if x['fact'] is not None else float('inf'))
    baseline = results[0]['fact'] if results and results[0]['fact'] else 1.0

    # CSV
    csv_path = os.path.join(RESULTS_DIR, "bigint_benchmark.csv")
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["Language", "Factorial Time (ms)", "Relative Speed", "Fibonacci Time (ms)", "Power Time (ms)", "Implementation Type"])
        for r in results:
            fact_s = f"{r['fact']:.4f}" if r['fact'] else "0"
            rel = f"{r['fact']/baseline:.2f}x" if r['fact'] else "0.00x"
            w.writerow([r['name'], fact_s, rel, f"{r['fib']:.4f}" if r['fib'] else "0", f"{r['pow']:.4f}" if r['pow'] else "0", r['type']])

    # Markdown Table
    md = "| Language | Factorial | Rel Speed | Fibonacci | Power | Type |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for r in results:
        fact_s = f"{r['fact']:.3f} ms" if r['fact'] else "—"
        rel = f"{r['fact']/baseline:.2f}x" if r['fact'] else "—"
        if r['fact'] == baseline: rel = "1.00x"
        md += f"| **{r['name']}** | {fact_s} | {rel} | {f'{r['fib']:.3f} ms' if r['fib'] else '—'} | {f'{r['pow']:.3f} ms' if r['pow'] else '—'} | {r['type']} |\n"
    
    append_report_section("BigInt Performance", md, "bigint.png")

def run_generic_bench(key, title, cmd_map, env, runs, csv_name, img_name):
    print(f"\n--- {title} ---")
    results = []
    for lang, cmd in cmd_map.items():
        t = run_benchmark_cmd(cmd, env, runs)
        results.append({"name": lang, "time": t})
    
    results.sort(key=lambda x: x['time'] if x['time'] is not None else float('inf'))
    baseline = next((r['time'] for r in results if r['time']), 1.0)

    # CSV
    with open(os.path.join(RESULTS_DIR, csv_name), 'w', newline='') as f:
        w = csv.writer(f)
        key_str = f"{key} Time (ms)"
        if key == "Float": key_str = "Float Time (50k iter)"
        w.writerow(["Language", key_str, "Relative Speed"])
        for r in results:
            w.writerow([r['name'], f"{r['time']:.4f}" if r['time'] else "0", f"{r['time']/baseline:.2f}x" if r['time'] else "0.00x"])

    # Markdown
    md = f"| Language | Time | Rel Speed |\n| :--- | :--- | :--- |\n"
    for r in results:
        t_s = f"{r['time']:.3f} ms" if r['time'] else "—"
        rel = f"{r['time']/baseline:.2f}x" if r['time'] else "—"
        if r['time'] == baseline: rel = "1.00x"
        md += f"| **{r['name']}** | {t_s} | {rel} |\n"
    
    append_report_section(title, md, img_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", choices=["all", "bigint", "float", "matrix", "sort"], default="all")
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()

    os.makedirs(RESULTS_DIR, exist_ok=True)
    
    if args.bench == "all":
        init_report()

    if args.bench in ["all", "bigint"]: run_bigint(args.runs)
    
    if args.bench in ["all", "float"]:
        targets = {
            "C": bin_cmd("float/fibo", "fibonacci", "c"), "C++": bin_cmd("float/fibo", "fibonacci", "cpp"),
            "Rust": bin_cmd("float/fibo", "fibonacci", "rs"), "Go": bin_cmd("float/fibo", "fibonacci", "go"),
            "Java": java_cmd("float/fibo", "FibonacciFloat"), "Python": py_cmd("fibonacci_float.py"),
            "JavaScript": js_cmd("fibonacci_float.js"), "Fortran": bin_cmd("float/fibo", "fibonacci", "f90"),
        }
        run_generic_bench("Float", "Float Throughput", targets, {"COUNT": DEFAULTS["float"]["count"]}, args.runs, "float_benchmark.csv", "float.png")

    if args.bench in ["all", "matrix"]:
        targets = {
            "Assembler": bin_cmd("matrix", "matrix", "asm"), "C": bin_cmd("matrix", "matrix", "c"),
            "C++": bin_cmd("matrix", "matrix", "cpp"), "Rust": bin_cmd("matrix", "matrix", "rs"),
            "Fortran": bin_cmd("matrix", "matrix", "f90"), "Go": bin_cmd("matrix", "matrix", "go"),
            "Java": java_cmd("matrix", "Matrix"), "JavaScript": js_cmd("matrix.js"), "Python": py_cmd("matrix.py"),
        }
        run_generic_bench("Matrix", "Matrix Multiplication", targets, {"MATRIX_SIZE": DEFAULTS["matrix"]["size"]}, args.runs, "matrix_benchmark.csv", "matrix.png")

    if args.bench in ["all", "sort"]:
        targets = {
            "Assembler": bin_cmd("sort", "bubble", "asm"), "C": bin_cmd("sort", "bubble", "c"),
            "C++": bin_cmd("sort", "bubble", "cpp"), "Rust": bin_cmd("sort", "bubble", "rs"),
            "Fortran": bin_cmd("sort", "bubble", "f90"), "Go": bin_cmd("sort", "bubble", "go"),
            "Java": java_cmd("sort", "Bubble"), "JavaScript": js_cmd("bubble.js"), "Python": py_cmd("bubble.py"),
        }
        run_generic_bench("Sort", "Bubble Sort", targets, {"SORT_SIZE": DEFAULTS["sort"]["size"]}, args.runs, "sort_benchmark.csv", "sort.png")

    print("\n--- Generating Plots ---")
    subprocess.run(["python3", "tests/plot.py"])
    print(f"Done! Check {REPORT_FILE}")

if __name__ == "__main__":
    main()
