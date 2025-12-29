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
        return None
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
            print(f"[SUCCESS] Updated README.md")
    except:
        pass

def benchmark():
    FIBO_COUNT = "5000"
    FACT_COUNT = "2000"
    POWER_BASE = "2"
    POWER_EXP = "5000"

    print(f"\n--- 1. BigInt Benchmark ---")
    
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
        t_f = run_command(lang['fib'], {"COUNT": FIBO_COUNT})
        t_fa = run_command(lang['fact'], {"COUNT": FACT_COUNT})
        t_p = run_command(lang['pow'], {"BASE": POWER_BASE, "EXP": POWER_EXP})
        results.append({**lang, "fibo": t_f, "fact": t_fa, "pow": t_p})

    results.sort(key=lambda x: x['fact'] if x['fact'] is not None else 999999999)
    baseline_fact = results[0]['fact'] if results and results[0]['fact'] else 1.0

    md = "| Language | Factorial (2000) | Rel Speed | Fibonacci (5000) | Power (2^5000) | BigInt Type |\n"
    md += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    print(f"{'Language':<12} | {'Fact (2000)':<12} | {'Rel Speed':<10} | {'Fibo (5000)':<12} | {'Pow':<10}")
    print("-" * 70)

    for r in results:
        s_fact = f"{r['fact']:.3f} ms" if r['fact'] is not None else "—"
        s_fibo = f"{r['fibo']:.3f} ms" if r['fibo'] is not None else "—"
        s_pow = f"{r['pow']:.3f} ms" if r['pow'] is not None else "—"
        rel_str = "—"
        if r['fact'] is not None:
            if r['fact'] == baseline_fact: rel_str = "1.00x"
            else: rel_str = f"{r['fact'] / baseline_fact:.2f}x"
        
        print(f"{r['name']:<12} | {s_fact:<12} | {rel_str:<10} | {s_fibo:<12} | {s_pow:<10}")
        md += f"| **{r['name']}** | {s_fact} | {rel_str} | {s_fibo} | {s_pow} | {r['type']} |\n"

    update_readme_section(md, "<!-- BENCHMARK_BIGINT_START -->", "<!-- BENCHMARK_BIGINT_END -->")

if __name__ == "__main__":
    benchmark()
