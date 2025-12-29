import subprocess
import os
import sys
import re
import statistics
import csv

# Configuration
RUNS = 5
CSV_FILE = "results/bigint_benchmark.csv"

def run_once(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        match = re.search(r"Time: ([0-9\.\-eE]+) ms", result.stdout)
        if match:
            return float(match.group(1))
        return None
    except:
        return None

def run_command(cmd, env_vars):
    times = []
    for _ in range(RUNS):
        t = run_once(cmd, env_vars)
        if t is not None:
            times.append(t)
    
    if not times:
        return None
    
    return statistics.median(times)

def update_readme_section(content, marker_start, marker_end):
    readme_path = "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
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
            with open(readme_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            # print(f"[SUCCESS] Updated README.md (BigInt)")
    except:
        pass

def save_csv(results, baseline_fact):
    try:
        os.makedirs("results", exist_ok=True)
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Language", "Factorial Time (ms)", "Relative Speed", "Fibonacci Time (ms)", "Power Time (ms)", "Implementation Type"])
            
            for r in results:
                fact = r['fact'] if r['fact'] else 0
                fibo = r['fibo'] if r['fibo'] else 0
                pow_t = r['pow'] if r['pow'] else 0
                
                rel_speed = 0
                if r['fact'] is not None:
                    rel_speed = r['fact'] / baseline_fact
                
                writer.writerow([r['name'], f"{fact:.4f}", f"{rel_speed:.2f}x", f"{fibo:.4f}", f"{pow_t:.4f}", r['type']])
        print(f"[SUCCESS] Saved CSV to {CSV_FILE}")
    except Exception as e:
        print(f"[ERROR] Could not save CSV: {e}")

def benchmark():
    FIBO_COUNT = "25000"
    FACT_COUNT = "5000"
    POWER_BASE = "2"
    POWER_EXP = "20000"

    print(f"\n--- 1. BigInt Benchmark (Median of {RUNS} runs) ---")
    
    languages = [
        {"name": "C",         "fib": "./bin/fibo/fibonacci_c",   "fact": "./bin/fact/factorial_c",   "pow": "./bin/power/power_c",   "type": "Custom Base 10^9"},
        {"name": "C++",       "fib": "./bin/fibo/fibonacci_cpp", "fact": "./bin/fact/factorial_cpp", "pow": "./bin/power/power_cpp", "type": "Custom Base 10^9"},
        {"name": "Rust",      "fib": "./bin/fibo/fibonacci_rs",  "fact": "./bin/fact/factorial_rs",  "pow": "./bin/power/power_rs",  "type": "Custom Base 10^9"},
        {"name": "Go",        "fib": "./bin/fibo/fibonacci_go",  "fact": "./bin/fact/factorial_go",  "pow": "./bin/power/power_go",  "type": "math/big"},
        {"name": "Java",      "fib": "java -cp bin/fibo Fibonacci", "fact": "java -cp bin/fact Factorial", "pow": "java -cp bin/power Power", "type": "BigInteger"},
        {"name": "Python",    "fib": "python3 src/python/fibonacci.py", "fact": "python3 src/python/factorial.py", "pow": "python3 src/python/power.py", "type": "Native"},
        {"name": "JavaScript","fib": "node src/js/fibonacci.js", "fact": "node src/js/factorial.js", "pow": "node src/js/power.js", "type": "BigInt"},
        {"name": "Fortran",   "fib": "./bin/fibo/fibonacci_f90", "fact": "./bin/fact/factorial_f90", "pow": "./bin/power/power_f90", "type": "Custom Base 10^9"},
    ]

    results = []
    for lang in languages:
        # print(f"Benchmarking {lang['name']}...", end="", flush=True)
        t_f = run_command(lang['fib'], {"COUNT": FIBO_COUNT})
        t_fa = run_command(lang['fact'], {"COUNT": FACT_COUNT})
        t_p = run_command(lang['pow'], {"BASE": POWER_BASE, "EXP": POWER_EXP})
        # print(f" Done")
        results.append({**lang, "fibo": t_f, "fact": t_fa, "pow": t_p})

    results.sort(key=lambda x: x['fact'] if x['fact'] is not None else 999999999)
    baseline_fact = results[0]['fact'] if results and results[0]['fact'] else 1.0

    save_csv(results, baseline_fact)

    md = f"| Language | Factorial ({FACT_COUNT}) | Rel Speed | Fibonacci ({FIBO_COUNT}) | Power (2^{POWER_EXP}) | BigInt Type |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    print("-" * 95)
    print(f"{'Language':<12} | {'Fact':<12} | {'Rel Speed':<10} | {'Fibo':<12} | {'Pow':<10} | {'Type'}")
    print("-" * 95)

    for r in results:
        s_fact = f"{r['fact']:.3f} ms" if r['fact'] is not None else "—"
        s_fibo = f"{r['fibo']:.3f} ms" if r['fibo'] is not None else "—"
        s_pow = f"{r['pow']:.3f} ms" if r['pow'] is not None else "—"
        rel_str = "—"
        if r['fact'] is not None:
            if r['fact'] == baseline_fact: rel_str = "1.00x"
            else: rel_str = f"{r['fact'] / baseline_fact:.2f}x"
        
        print(f"{r['name']:<12} | {s_fact:<12} | {rel_str:<10} | {s_fibo:<12} | {s_pow:<10} | {r['type']}")
        md += f"| **{r['name']}** | {s_fact} | {rel_str} | {s_fibo} | {s_pow} | {r['type']} |\n"

    update_readme_section(md, "<!-- BENCHMARK_BIGINT_START -->", "<!-- BENCHMARK_BIGINT_END -->")
    print(f"[SUCCESS] Updated README.md (BigInt)")

if __name__ == "__main__":
    benchmark()
