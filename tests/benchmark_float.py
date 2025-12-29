import subprocess
import os
import sys
import re

def run_command(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        match = re.search(r"Time: ([0-9\.\-eE]+) ms", result.stdout)
        if match:
            return float(match.group(1))
        return 0.0 # Capture fast times as 0.0 usually, but logic below handles it
    except:
        return None

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
            print(f"[SUCCESS] Updated {marker_start} in README.md")
    except:
        pass

def benchmark_float():
    FIBO = "1475"
    
    print(f"--- Running Float Comparison Benchmark ---")

    languages = [
        {"name": "C++", "b": "./bin/fibo/fibonacci_cpp", "f": "./bin/float/fibo/fibonacci_cpp"},
        {"name": "Rust", "b": "./bin/fibo/fibonacci_rs", "f": "./bin/float/fibo/fibonacci_rs"},
        {"name": "Go", "b": "./bin/fibo/fibonacci_go", "f": "./bin/float/fibo/fibonacci_go"},
        {"name": "Java", "b": "java -cp bin/fibo Fibonacci", "f": "java -cp bin/float/fibo FibonacciFloat"},
        {"name": "Python", "b": "python3 src/python/fibonacci.py", "f": "python3 src/python/fibonacci_float.py"},
        {"name": "JavaScript", "b": "node src/js/fibonacci.js", "f": "node src/js/fibonacci_float.js"},
        {"name": "Fortran", "b": "./bin/fibo/fibonacci_f90", "f": "./bin/float/fibo/fibonacci_f90"},
    ]

    results = []
    for lang in languages:
        t_big = run_command(lang['b'], {"COUNT": FIBO})
        t_flt = run_command(lang['f'], {"COUNT": FIBO})
        results.append({
            "name": lang['name'],
            "big": t_big,
            "flt": t_flt
        })

    # Sort by Float Time (fastest first)
    # Treat None or 0.0 (too fast) carefully. 
    # If 0.0, it is fastest.
    results.sort(key=lambda x: x['flt'] if x['flt'] is not None else 999999.0)

    # Determine baseline (fastest float time that isn't 0 if possible, or just min)
    # Note: If C++ gives 0.000, it's the baseline.
    baseline_val = results[0]['flt']
    if baseline_val == 0: baseline_val = 0.0000001 # Avoid division by zero

    md = "| Language | Float Time | Rel Speed | BigInt Time | Hardware Speedup |\n"
    md += "| :--- | :--- | :--- | :--- | :--- |\n"

    for r in results:
        # Time strings
        s_big = f"{r['big']:.3f} ms" if r['big'] is not None else "—"
        s_flt = f"{r['flt']:.4f} ms" if r['flt'] is not None else "—"
        
        # Speedup (BigInt vs Float within same lang)
        speedup = "—"
        if r['big'] is not None and r['flt'] is not None and r['flt'] > 0:
            speedup = f"{r['big']/r['flt']:.1f}x"
        elif r['big'] is not None and r['flt'] == 0:
            speedup = "Max"

        # Relative (Lang vs Lang Baseline)
        rel = "—"
        if r['flt'] is not None:
            val = r['flt']
            if val <= baseline_val: # Handle close to 0
                 rel = "1.00x"
            else:
                 rel = f"{val/baseline_val:.2f}x"

        md += f"| **{r['name']}** | {s_flt} | {rel} | {s_big} | {speedup} |\n"

    update_readme_section(md, "<!-- BENCHMARK_FLOAT_START -->", "<!-- BENCHMARK_FLOAT_END -->")

if __name__ == "__main__":
    benchmark_float()
