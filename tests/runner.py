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
README_FILE = "README.md"

# Default Inputs (Can be overridden via env vars in the specific run logic)
DEFAULTS = {
    "bigint": {
        "fib": "25000",
        "fact": "5000",
        "base": "2",
        "exp": "20000"
    },
    "float": {
        "count": "1475",
        "loops": "200000" # Logic handled inside source code
    },
    "matrix": {
        "size": "600"
    },
    "sort": {
        "size": "10000"
    }
}

# --- Command Definitions ---
# Helper to form commands
def bin_cmd(folder, name, ext=""):
    # e.g. ./bin/fibo/fibonacci_c
    return f"./bin/{folder}/{name}_{ext}"

def java_cmd(folder, class_name):
    return f"java -cp bin/{folder} {class_name}"

def py_cmd(script):
    return f"python3 src/python/{script}"

def js_cmd(script):
    return f"node src/js/{script}"

# Language Definitions & Commands
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

# --- Helper Functions ---

def parse_time(stdout):
    """Extracts 'Time: 123.456 ms' from output."""
    match = re.search(r"Time: ([0-9\.\-eE]+) ms", stdout)
    if match:
        return float(match.group(1))
    return None

def run_once(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        # Shell=True allows complex commands, but we must be careful with inputs
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        return parse_time(result.stdout)
    except Exception as e:
        print(f"Error running {cmd}: {e}")
        return None

def run_benchmark_cmd(cmd, env_vars, runs):
    times = []
    for _ in range(runs):
        t = run_once(cmd, env_vars)
        if t is not None:
            times.append(t)
    if not times:
        return None
    return statistics.median(times)

def update_readme(marker_start, marker_end, content):
    if not os.path.exists(README_FILE):
        return
    
    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    skip = False
    found = False
    
    for line in lines:
        if marker_start in line:
            new_lines.append(line)
            new_lines.append(content + "\n")
            skip = True
            found = True
            continue
        if marker_end in line:
            skip = False
            new_lines.append(line)
            continue
        if not skip:
            new_lines.append(line)
            
    if found:
        with open(README_FILE, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Updated {README_FILE} section {marker_start}")

# --- Benchmark Implementations ---

def run_bigint(runs):
    print(f"\n--- 1. BigInt Benchmark (Median of {runs} runs) ---")
    
    # Structure: (fib_cmd, fact_cmd, pow_cmd)
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
        # print(f"Benchmarking {name}...", flush=True)
        t_f = run_benchmark_cmd(cmd_f, env_fib, runs)
        t_fa = run_benchmark_cmd(cmd_fa, env_fact, runs)
        t_p = run_benchmark_cmd(cmd_p, env_pow, runs)
        
        # Determine BigInt Type from LANGS dict
        b_type = next((v["type"] for k, v in LANGS.items() if v["name"] == name), "Unknown")
        
        results.append({
            "name": name, 
            "fib": t_f, 
            "fact": t_fa, 
            "pow": t_p,
            "type": b_type
        })

    # Sort by Factorial Time
    results.sort(key=lambda x: x['fact'] if x['fact'] is not None else float('inf'))
    baseline = results[0]['fact'] if results and results[0]['fact'] else 1.0

    # CSV
    csv_path = os.path.join(RESULTS_DIR, "bigint_benchmark.csv")
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["Language", "Factorial Time (ms)", "Relative Speed", "Fibonacci Time (ms)", "Power Time (ms)", "Implementation Type"])
        for r in results:
            fact_s = f"{r['fact']:.4f}" if r['fact'] else "0"
            fib_s = f"{r['fib']:.4f}" if r['fib'] else "0"
            pow_s = f"{r['pow']:.4f}" if r['pow'] else "0"
            rel = f"{r['fact']/baseline:.2f}x" if r['fact'] else "0.00x"
            w.writerow([r['name'], fact_s, rel, fib_s, pow_s, r['type']])
    print(f"Saved {csv_path}")

    # README MD
    md_lines = [
        f"| Language | Factorial ({DEFAULTS['bigint']['fact']}) | Rel Speed | Fibonacci ({DEFAULTS['bigint']['fib']}) | Power ({DEFAULTS['bigint']['base']}^{DEFAULTS['bigint']['exp']}) | BigInt Type |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    # Print Table
    print(f"{'Language':<12} | {'Fact':<10} | {'Rel':<8} | {'Fibo':<10} | {'Pow':<10} | {'Type'}")
    print("-" * 75)
    
    for r in results:
        fact_s = f"{r['fact']:.3f} ms" if r['fact'] else "—"
        fib_s = f"{r['fib']:.3f} ms" if r['fib'] else "—"
        pow_s = f"{r['pow']:.3f} ms" if r['pow'] else "—"
        
        rel = "—"
        if r['fact']:
             rel = "1.00x" if r['fact'] == baseline else f"{r['fact']/baseline:.2f}x"

        print(f"{r['name']:<12} | {fact_s:<10} | {rel:<8} | {fib_s:<10} | {pow_s:<10} | {r['type']}")
        md_lines.append(f"| **{r['name']}** | {fact_s} | {rel} | {fib_s} | {pow_s} | {r['type']} |")

    update_readme("<!-- BENCHMARK_BIGINT_START -->", "<!-- BENCHMARK_BIGINT_END -->", "\n".join(md_lines))


def run_simple_bench(name_key, title, cmd_map, env, runs, csv_name, md_header, baseline_key="time"):
    """Generic function for Float, Matrix, Sort."""
    print(f"\n--- {title} (Median of {runs} runs) ---")
    
    results = []
    for lang_name, cmd in cmd_map.items():
        t = run_benchmark_cmd(cmd, env, runs)
        results.append({"name": lang_name, "time": t})

    # Sort
    results.sort(key=lambda x: x['time'] if x['time'] is not None else float('inf'))
    baseline = results[0]['time'] if results and results[0]['time'] else 1.0

    # CSV
    csv_path = os.path.join(RESULTS_DIR, csv_name)
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(["Language", f"{name_key} Time (ms)", "Relative Speed"])
        for r in results:
            t_s = f"{r['time']:.4f}" if r['time'] else "0"
            rel = f"{r['time']/baseline:.2f}x" if r['time'] else "0.00x"
            w.writerow([r['name'], t_s, rel])
    print(f"Saved {csv_path}")

    # README & Console
    md_lines = [md_header, "| :--- | :--- | :--- |"]
    print(f"{'Language':<12} | {'Time':<12} | {'Rel Speed':<10}")
    print("-" * 40)

    for r in results:
        t_s = f"{r['time']:.1f} ms" if r['time'] else "—" # Less precision for visual table
        if name_key == "Matrix" or name_key == "Sort":
             t_s = f"{r['time']:.3f} ms" if r['time'] else "—"

        rel = "—"
        if r['time']:
            rel = "1.00x" if r['time'] == baseline else f"{r['time']/baseline:.2f}x"
        
        print(f"{r['name']:<12} | {t_s:<12} | {rel:<10}")
        md_lines.append(f"| **{r['name']}** | {t_s} | {rel} |")

    return "\n".join(md_lines)

def run_float(runs):
    targets = {
        "C":          bin_cmd("float/fibo", "fibonacci", "c"),
        "C++":        bin_cmd("float/fibo", "fibonacci", "cpp"),
        "Rust":       bin_cmd("float/fibo", "fibonacci", "rs"),
        "Go":         bin_cmd("float/fibo", "fibonacci", "go"),
        "Java":       java_cmd("float/fibo", "FibonacciFloat"),
        "Python":     py_cmd("fibonacci_float.py"),
        "JavaScript": js_cmd("fibonacci_float.js"),
        "Fortran":    bin_cmd("float/fibo", "fibonacci", "f90"),
    }
    env = {"COUNT": DEFAULTS["float"]["count"]}
    md = run_simple_bench("Float", "2. Float Benchmark", targets, env, runs, 
                          "float_benchmark.csv", 
                          "| Language | Float Time (200k iter) | Rel Speed |")
    update_readme("<!-- BENCHMARK_FLOAT_START -->", "<!-- BENCHMARK_FLOAT_END -->", md)

def run_matrix(runs):
    targets = {
        "Assembler":  bin_cmd("matrix", "matrix", "asm"),
        "C":          bin_cmd("matrix", "matrix", "c"),
        "C++":        bin_cmd("matrix", "matrix", "cpp"),
        "Rust":       bin_cmd("matrix", "matrix", "rs"),
        "Fortran":    bin_cmd("matrix", "matrix", "f90"),
        "Go":         bin_cmd("matrix", "matrix", "go"),
        "Java":       java_cmd("matrix", "Matrix"),
        "JavaScript": js_cmd("matrix.js"),
        "Python":     py_cmd("matrix.py"),
    }
    env = {"MATRIX_SIZE": DEFAULTS["matrix"]["size"]}
    md = run_simple_bench("Matrix", f"3. Matrix Benchmark ({env['MATRIX_SIZE']}x{env['MATRIX_SIZE']})", 
                          targets, env, runs, 
                          "matrix_benchmark.csv", 
                          f"| Language | Matrix Mult ({env['MATRIX_SIZE']}x{env['MATRIX_SIZE']}) | Relative Speed |")
    update_readme("<!-- BENCHMARK_MATRIX_START -->", "<!-- BENCHMARK_MATRIX_END -->", md)

def run_sort(runs):
    targets = {
        "Assembler":  bin_cmd("sort", "bubble", "asm"),
        "C":          bin_cmd("sort", "bubble", "c"),
        "C++":        bin_cmd("sort", "bubble", "cpp"),
        "Rust":       bin_cmd("sort", "bubble", "rs"),
        "Fortran":    bin_cmd("sort", "bubble", "f90"),
        "Go":         bin_cmd("sort", "bubble", "go"),
        "Java":       java_cmd("sort", "Bubble"),
        "JavaScript": js_cmd("bubble.js"),
        "Python":     py_cmd("bubble.py"),
    }
    env = {"SORT_SIZE": DEFAULTS["sort"]["size"]}
    md = run_simple_bench("Sort", f"4. Bubble Sort Benchmark (N={env['SORT_SIZE']})", 
                          targets, env, runs, 
                          "sort_benchmark.csv", 
                          f"| Language | Bubble Sort ({env['SORT_SIZE']}) | Relative Speed |")
    update_readme("<!-- BENCHMARK_SORT_START -->", "<!-- BENCHMARK_SORT_END -->", md)

# --- Main CLI ---

def main():
    parser = argparse.ArgumentParser(description="Polyglot Benchmark Runner")
    parser.add_argument("--bench", choices=["all", "bigint", "float", "matrix", "sort"], default="all", help="Which benchmark to run")
    parser.add_argument("--runs", type=int, default=5, help="Number of runs per test for median calculation")
    
    args = parser.parse_args()

    # Create results dir
    os.makedirs(RESULTS_DIR, exist_ok=True)

    if args.bench == "all" or args.bench == "bigint":
        run_bigint(args.runs)
    
    if args.bench == "all" or args.bench == "float":
        run_float(args.runs)
        
    if args.bench == "all" or args.bench == "matrix":
        run_matrix(args.runs)
        
    if args.bench == "all" or args.bench == "sort":
        run_sort(args.runs)

if __name__ == "__main__":
    main()
