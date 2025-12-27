import os
import subprocess
import sys

# Increase limit for integer to string conversion
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(1000000)

def calculate_fibonacci(n):
    if n <= 0: return 0
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def run_command(cmd, count):
    env = os.environ.copy()
    env["COUNT"] = str(count)
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def get_result_from_output(output):
    for line in output.split('\n'):
        if "Result" in line:
            return line.split(':')[-1].strip()
    return None

def verify():
    count = 1000
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    
    true_val = str(calculate_fibonacci(count))
    
    languages = [
        {"name": "C++", "cmd": "./bin/fibo/fibonacci_cpp"},
        {"name": "Go", "cmd": "./bin/fibo/fibonacci_go"},
        {"name": "Rust", "cmd": "./bin/fibo/fibonacci_rs"},
        {"name": "Java", "cmd": "java -cp bin/fibo Fibonacci"},
        {"name": "Fortran", "cmd": "./bin/fibo/fibonacci_f90"},
        {"name": "Python", "cmd": "python3 src/python/fibonacci.py"},
        {"name": "JavaScript", "cmd": "node src/js/fibonacci.js"},
    ]

    print(f"--- Verifying Fibonacci up to {count} ---")
    
    all_passed = True
    for lang in languages:
        output = run_command(lang["cmd"], count)
        result = get_result_from_output(output)
        
        expected = true_val
        status = "PASSED" if result == expected else "FAILED"
        
        if status == "FAILED":
            all_passed = False
            print(f"[{lang['name']}] {status}")
            print(f"  Expected: {expected[:50]}... (len={len(expected)})")
            print(f"  Got:      {result[:50] if result else 'None'}... (len={len(result) if result else 0})")
        else:
            print(f"[{lang['name']}] {status} (N={count})")

    if all_passed:
        print("\nAll languages verified correctly!")
    else:
        print("\nSome verifications failed.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
