import os
import subprocess
import sys
import math

# Increase limit for integer to string conversion
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(1000000)

def calculate_factorial(n):
    return math.factorial(n)

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
    count = 200
    if len(sys.argv) > 1:
        count = int(sys.argv[1])
    
    true_val = str(calculate_factorial(count))
    
    languages = [
        {"name": "C++", "cmd": "./bin/fact/factorial_cpp", "is_fixed": False},
        {"name": "Go", "cmd": "./bin/fact/factorial_go", "is_fixed": False},
        {"name": "Rust", "cmd": "./bin/fact/factorial_rs", "is_fixed": False},
        {"name": "Java", "cmd": "java -cp bin/fact Factorial", "is_fixed": False},
        {"name": "Fortran", "cmd": "./bin/fact/factorial_f90", "is_fixed": False},
        {"name": "Python", "cmd": "python3 src/python/factorial.py", "is_fixed": False},
        {"name": "JavaScript", "cmd": "node src/js/factorial.js", "is_fixed": False},
    ]

    print(f"--- Verifying Factorial up to {count} ---")
    
    all_passed = True
    for lang in languages:
        output = run_command(lang["cmd"], count)
        result = get_result_from_output(output)
        
        target_count = count
        if lang["is_fixed"] and count > lang["max"]:
            target_count = lang["max"]
            expected = str(calculate_factorial(target_count))
            status = "FIXED-WIDTH (Correct Overflow)" if result == expected else "FAILED"
        else:
            expected = str(calculate_factorial(target_count))
            status = "PASSED" if result == expected else "FAILED"
        
        if status == "FAILED":
            all_passed = False
            print(f"[{lang['name']}] {status}")
            print(f"  Expected: {expected[:50]}...")
            print(f"  Got:      {result[:50] if result else 'None'}...")
        else:
            print(f"[{lang['name']}] {status} (N={target_count})")

    if all_passed:
        print("\nAll languages verified correctly!")
    else:
        print("\nSome verifications failed.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
