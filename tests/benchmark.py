import subprocess
import os
import sys
import re

def run_command(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        # Run command and capture output
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        output = result.stdout
        
        # Parse Time
        match = re.search(r"Time: (\d+\.\d+) ms", output)
        if match:
            return float(match.group(1))
        return None
    except Exception as e:
        return None

def update_readme(table_content):
    readme_path = "README.md"
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        in_table = False
        table_inserted = False
        
        for line in lines:
            # Detect start of table
            if "| Language | Fibonacci" in line:
                in_table = True
                
            # If we are in table and see a line that doesn't start with |, table ends
            if in_table and not line.strip().startswith("|"):
                in_table = False
                # Insert new table here if not already inserted
                if not table_inserted:
                    new_lines.append(table_content)
                    table_inserted = True
            
            if not in_table:
                new_lines.append(line)
        
        # If table was at the very end
        if in_table and not table_inserted:
             new_lines.append(table_content)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
            
        print("\n[SUCCESS] README.md updated with new benchmark results.")
        
    except Exception as e:
        print(f"\n[ERROR] Could not update README.md: {e}")

def benchmark():
    # Parameters for the benchmark
    FIBO_COUNT = "5000"
    FACT_COUNT = "2000"
    POWER_BASE = "2"
    POWER_EXP = "5000"

    print(f"Running Benchmarks...")
    print(f"Fibonacci: {FIBO_COUNT}")
    print(f"Factorial: {FACT_COUNT}")
    print(f"Power: {POWER_BASE}^{POWER_EXP}")
    print("-" * 60)

    languages = [
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
        print(f"Benchmarking {lang['name']}...", end="", flush=True)
        
        t_fibo = run_command(lang['fib'], {"COUNT": FIBO_COUNT})
        t_fact = run_command(lang['fact'], {"COUNT": FACT_COUNT})
        t_pow = run_command(lang['pow'], {"BASE": POWER_BASE, "EXP": POWER_EXP})
        
        results.append({
            "name": lang['name'],
            "fibo": t_fibo,
            "fact": t_fact,
            "pow": t_pow,
            "type": lang['type']
        })
        print(" Done.")

    # Generate Markdown Table String
    md_output = f"| Language | Fibonacci ({FIBO_COUNT}) | Factorial ({FACT_COUNT}) | Power ({POWER_BASE}^{POWER_EXP}) | BigInt Type |\n"
    md_output += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for r in results:
        f_str = f"{r['fibo']:.3f} ms" if r['fibo'] is not None else "—"
        fact_str = f"{r['fact']:.3f} ms" if r['fact'] is not None else "—"
        pow_str = f"{r['pow']:.3f} ms" if r['pow'] is not None else "—"
        
        md_output += f"| **{r['name']}** | {f_str} | {fact_str} | {pow_str} | {r['type']} |\n"

    print("\n--- Markdown Report ---")
    print(md_output)
    
    # Update README
    update_readme(md_output)

if __name__ == "__main__":
    benchmark()
