import subprocess
import os
import sys
import re
import statistics
import csv

RUNS = 5
CSV_FILE = "results/float_benchmark.csv"

def run_once(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        match = re.search(r"Time: ([0-9\.\-eE]+) ms", result.stdout)
        if match:
            return float(match.group(1))
        return 0.0
    except:
        return None

def run_command(cmd, env_vars):
    times = []
    for _ in range(RUNS):
        t = run_once(cmd, env_vars)
        if t is not None: times.append(t)
    if not times: return None
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
            # print(f"[SUCCESS] Updated README.md (Float)")
    except:
        pass

def save_csv(results, baseline_val):
    try:
        os.makedirs("results", exist_ok=True)
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Language", "Float Time (ms)", "Relative Speed"])
            
            for r in results:
                t = r['flt'] if r['flt'] else 0
                rel_speed = 0
                if r['flt'] is not None:
                     rel_speed = r['flt'] / baseline_val
                
                writer.writerow([r['name'], f"{t:.4f}", f"{rel_speed:.2f}x"])
        print(f"[SUCCESS] Saved CSV to {CSV_FILE}")
    except Exception as e:
        print(f"[ERROR] Could not save CSV: {e}")

def benchmark_float():
    FIBO = "1475"
    print(f"\n--- 2. Float Benchmark (200k iterations, Median of {RUNS} runs) ---")

    languages = [
        {"name": "C", "f": "./bin/float/fibo/fibonacci_c"},
        {"name": "C++", "f": "./bin/float/fibo/fibonacci_cpp"},
        {"name": "Rust", "f": "./bin/float/fibo/fibonacci_rs"},
        {"name": "Go", "f": "./bin/float/fibo/fibonacci_go"},
        {"name": "Java", "f": "java -cp bin/float/fibo FibonacciFloat"},
        {"name": "Python", "f": "python3 src/python/fibonacci_float.py"},
        {"name": "JavaScript", "f": "node src/js/fibonacci_float.js"},
        {"name": "Fortran", "f": "./bin/float/fibo/fibonacci_f90"},
    ]

    results = []
    for lang in languages:
        t_flt = run_command(lang['f'], {"COUNT": FIBO})
        results.append({"name": lang['name'], "flt": t_flt})

    results.sort(key=lambda x: x['flt'] if x['flt'] is not None else 999999.0)
    baseline_val = results[0]['flt']
    if baseline_val == 0: baseline_val = 0.0000001
    
    save_csv(results, baseline_val)

    md = "| Language | Float Time (200k iter) | Rel Speed |\n"
    md += "| :--- | :--- | :--- |\n"

    print("-" * 50)
    print(f"{'Language':<12} | {'Float Time':<12} | {'Rel Speed':<10}")
    print("-" * 50)

    for r in results:
        s_flt = f"{r['flt']:.1f} ms" if r['flt'] is not None else "—"
        rel = "—"
        if r['flt'] is not None:
            val = r['flt']
            if val <= baseline_val: rel = "1.00x"
            else: rel = f"{val/baseline_val:.2f}x"
        
        print(f"{r['name']:<12} | {s_flt:<12} | {rel:<10}")
        md += f"| **{r['name']}** | {s_flt} | {rel} |\n"

    update_readme_section(md, "<!-- BENCHMARK_FLOAT_START -->", "<!-- BENCHMARK_FLOAT_END -->")
    print(f"[SUCCESS] Updated README.md (Float)")

if __name__ == "__main__":
    benchmark_float()
