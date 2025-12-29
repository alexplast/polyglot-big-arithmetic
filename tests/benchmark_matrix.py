import subprocess
import os
import sys
import re
import statistics
import csv

RUNS = 5
CSV_FILE = "results/matrix_benchmark.csv"

def run_once(cmd, n_size):
    env = os.environ.copy()
    env["MATRIX_SIZE"] = str(n_size)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        if result.returncode != 0: return None
        match = re.search(r"Time: ([0-9\.\-eE]+) ms", result.stdout)
        if match: return float(match.group(1))
        return None
    except:
        return None

def run_command(cmd, n_size):
    times = []
    for _ in range(RUNS):
        t = run_once(cmd, n_size)
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
            # print(f"[SUCCESS] Updated README.md (Matrix)")
    except:
        pass

def save_csv(results, fastest_time):
    try:
        os.makedirs("results", exist_ok=True)
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Language", "Matrix Time (ms)", "Relative Speed"])
            
            for r in results:
                name, t = r
                t_val = t if t else 0
                rel_speed = 0
                if t is not None and fastest_time:
                     rel_speed = t / fastest_time
                
                writer.writerow([name, f"{t_val:.4f}", f"{rel_speed:.2f}x"])
        print(f"[SUCCESS] Saved CSV to {CSV_FILE}")
    except Exception as e:
        print(f"[ERROR] Could not save CSV: {e}")

def benchmark_matrix():
    N = 600
    print(f"\n--- 3. Matrix Benchmark (N={N}, Median of {RUNS} runs) ---")
    
    languages = [
        {"name": "Assembler", "cmd": "./bin/matrix/matrix_asm"},
        {"name": "C", "cmd": "./bin/matrix/matrix_c"},
        {"name": "C++", "cmd": "./bin/matrix/matrix_cpp"},
        {"name": "Rust", "cmd": "./bin/matrix/matrix_rs"},
        {"name": "Fortran", "cmd": "./bin/matrix/matrix_f90"},
        {"name": "Go", "cmd": "./bin/matrix/matrix_go"},
        {"name": "Java", "cmd": "java -cp bin/matrix Matrix"},
        {"name": "JavaScript", "cmd": "node src/js/matrix.js"},
        {"name": "Python", "cmd": "python3 src/python/matrix.py"},
    ]

    results = []
    for lang in languages:
        # print(f"Benchmarking {lang['name']}...", end="", flush=True)
        time_ms = run_command(lang['cmd'], N)
        # print(f" Done")
        results.append((lang['name'], time_ms))

    results.sort(key=lambda x: x[1] if x[1] is not None else 99999999)
    fastest_time = results[0][1] if results and results[0][1] else 1.0

    save_csv(results, fastest_time)

    md = f"| Language | Matrix Mult ({N}x{N}) | Relative Speed |\n"
    md += "| :--- | :--- | :--- |\n"
    
    print("-" * 50)
    print(f"{'Language':<12} | {'Time':<12} | {'Rel Speed':<10}")
    print("-" * 50)

    for name, t in results:
        t_str = f"{t:.3f} ms" if t is not None else "FAILED"
        if t is not None and fastest_time is not None:
            if t == fastest_time: rel = "1.00x"
            else: rel = f"{t / fastest_time:.2f}x"
        else: rel = "-"
        
        print(f"{name:<12} | {t_str:<12} | {rel:<10}")
        md += f"| **{name}** | {t_str} | {rel} |\n"

    update_readme_section(md, "<!-- BENCHMARK_MATRIX_START -->", "<!-- BENCHMARK_MATRIX_END -->")
    print(f"[SUCCESS] Updated README.md (Matrix)")

if __name__ == "__main__":
    benchmark_matrix()
