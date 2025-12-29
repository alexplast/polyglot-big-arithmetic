import subprocess
import os
import sys
import re

def run_command(cmd, env_vars):
    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        output = result.stdout
        
        # Updated Regex to handle:
        # 123.456
        # 0.00001
        # 1.23e-05
        match = re.search(r"Time: ([0-9\.\-eE]+) ms", output)
        if match:
            return float(match.group(1))
        return 0.0 # Return 0.0 instead of None if found but 0, or handle gracefully
    except Exception as e:
        return None

def benchmark_float():
    # Safe limits for IEEE 754 64-bit float (Universal for all languages)
    # Note: C++ and Fortran will use 128-bit/80-bit logic but run on these limits 
    # to maintain comparison parity.
    FIBO_COUNT = "1475"
    FACT_COUNT = "170"
    POWER_BASE = "2"
    POWER_EXP = "1023"

    print(f"Running FLOAT Benchmarks (Native CPU types)...")
    print(f"Fibonacci: {FIBO_COUNT}")
    print(f"Factorial: {FACT_COUNT}")
    print(f"Power: {POWER_BASE}^{POWER_EXP}")
    print("-" * 75)

    languages = [
        {
            "name": "C++",       
            "big_fib": "./bin/fibo/fibonacci_cpp", "big_fact": "./bin/fact/factorial_cpp", "big_pow": "./bin/power/power_cpp",
            "flt_fib": "./bin/float/fibo/fibonacci_cpp", "flt_fact": "./bin/float/fact/factorial_cpp", "flt_pow": "./bin/float/power/power_cpp"
        },
        {
            "name": "Rust",      
            "big_fib": "./bin/fibo/fibonacci_rs",  "big_fact": "./bin/fact/factorial_rs",  "big_pow": "./bin/power/power_rs",
            "flt_fib": "./bin/float/fibo/fibonacci_rs", "flt_fact": "./bin/float/fact/factorial_rs", "flt_pow": "./bin/float/power/power_rs"
        },
        {
            "name": "Fortran",   
            "big_fib": "./bin/fibo/fibonacci_f90", "big_fact": "./bin/fact/factorial_f90", "big_pow": "./bin/power/power_f90",
            "flt_fib": "./bin/float/fibo/fibonacci_f90", "flt_fact": "./bin/float/fact/factorial_f90", "flt_pow": "./bin/float/power/power_f90"
        },
        {
            "name": "Go",        
            "big_fib": "./bin/fibo/fibonacci_go",  "big_fact": "./bin/fact/factorial_go",  "big_pow": "./bin/power/power_go",
            "flt_fib": "./bin/float/fibo/fibonacci_go", "flt_fact": "./bin/float/fact/factorial_go", "flt_pow": "./bin/float/power/power_go"
        },
        {
            "name": "Java",      
            "big_fib": "java -cp bin/fibo Fibonacci", "big_fact": "java -cp bin/fact Factorial", "big_pow": "java -cp bin/power Power",
            "flt_fib": "java -cp bin/float/fibo FibonacciFloat", "flt_fact": "java -cp bin/float/fact FactorialFloat", "flt_pow": "java -cp bin/float/power PowerFloat"
        },
        {
            "name": "JavaScript",
            "big_fib": "node src/js/fibonacci.js", "big_fact": "node src/js/factorial.js", "big_pow": "node src/js/power.js",
            "flt_fib": "node src/js/fibonacci_float.js", "flt_fact": "node src/js/factorial_float.js", "flt_pow": "node src/js/power_float.js"
        },
        {
            "name": "Python",    
            "big_fib": "python3 src/python/fibonacci.py", "big_fact": "python3 src/python/factorial.py", "big_pow": "python3 src/python/power.py",
            "flt_fib": "python3 src/python/fibonacci_float.py", "flt_fact": "python3 src/python/factorial_float.py", "flt_pow": "python3 src/python/power_float.py"
        },
    ]

    print(f"{'Language':<12} | {'Alg':<5} | {'BigInt (ms)':<12} | {'Float (ms)':<12} | {'Speedup':<8}")
    print("-" * 75)

    for lang in languages:
        # Fibo
        t_big = run_command(lang['big_fib'], {"COUNT": FIBO_COUNT})
        t_flt = run_command(lang['flt_fib'], {"COUNT": FIBO_COUNT})
        
        ratio = "-"
        if t_big is not None and t_flt is not None:
            if t_flt == 0:
                ratio = "Inf" # Too fast to measure
            else:
                ratio = f"{t_big/t_flt:.1f}x"
                
        t_big_s = str(t_big) if t_big is not None else "None"
        t_flt_s = str(t_flt) if t_flt is not None else "None"
        
        print(f"{lang['name']:<12} | Fibo  | {t_big_s:<12} | {t_flt_s:<12} | {ratio}")

        # Fact
        t_big = run_command(lang['big_fact'], {"COUNT": FACT_COUNT})
        t_flt = run_command(lang['flt_fact'], {"COUNT": FACT_COUNT})
        
        ratio = "-"
        if t_big is not None and t_flt is not None:
            if t_flt == 0:
                ratio = "Inf"
            else:
                ratio = f"{t_big/t_flt:.1f}x"

        t_big_s = str(t_big) if t_big is not None else "None"
        t_flt_s = str(t_flt) if t_flt is not None else "None"

        print(f"{'':<12} | Fact  | {t_big_s:<12} | {t_flt_s:<12} | {ratio}")

        # Power
        t_big = run_command(lang['big_pow'], {"BASE": POWER_BASE, "EXP": POWER_EXP})
        t_flt = run_command(lang['flt_pow'], {"BASE": POWER_BASE, "EXP": POWER_EXP})
        
        ratio = "-"
        if t_big is not None and t_flt is not None:
            if t_flt == 0:
                ratio = "Inf"
            else:
                ratio = f"{t_big/t_flt:.1f}x"

        t_big_s = str(t_big) if t_big is not None else "None"
        t_flt_s = str(t_flt) if t_flt is not None else "None"

        print(f"{'':<12} | Pow   | {t_big_s:<12} | {t_flt_s:<12} | {ratio}")
        
        print("-" * 75)

if __name__ == "__main__":
    benchmark_float()
