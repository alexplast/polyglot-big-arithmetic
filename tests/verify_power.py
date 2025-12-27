import os
import subprocess
import sys

# Increase limit for integer to string conversion
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(1000000)

def calculate_power(base, exp):
    return pow(base, exp)

def run_command(cmd, base, exp):
    env = os.environ.copy()
    env["BASE"] = str(base)
    env["EXP"] = str(exp)
    result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def get_result_from_output(output):
    for line in output.split('\n'):
        if "Result" in line:
            return line.split(':')[-1].strip()
    return None

def verify():
    base = 2
    exp = 1000
    
    if len(sys.argv) > 1:
        base = int(sys.argv[1])
    if len(sys.argv) > 2:
        exp = int(sys.argv[2])
    
    true_val = str(calculate_power(base, exp))
    
    languages = [
        {"name": "C++", "cmd": "./bin/power/power_cpp"},
        {"name": "Go", "cmd": "./bin/power/power_go"},
        {"name": "Rust", "cmd": "./bin/power/power_rs"},
        {"name": "Java", "cmd": "java -cp bin/power Power"},
        {"name": "Fortran", "cmd": "./bin/power/power_f90"},
        {"name": "Python", "cmd": "python3 src/python/power.py"},
        {"name": "JavaScript", "cmd": "node src/js/power.js"},
    ]

    print(f"--- Verifying Power ({base}^{exp}) ---")
    
    all_passed = True
    for lang in languages:
        output = run_command(lang["cmd"], base, exp)
        result = get_result_from_output(output)
        
        if result == true_val:
            status = "PASSED"
        else:
            status = "FAILED"
            all_passed = False
        
        if status == "FAILED":
            print(f"[{lang['name']}] {status}")
            print(f"  Expected: {true_val[:50]}...")
            print(f"  Got:      {result[:50] if result else 'None'}...")
        else:
            print(f"[{lang['name']}] {status}")

    if all_passed:
        print("\nAll languages verified correctly!")
    else:
        print("\nSome verifications failed.")
        sys.exit(1)

if __name__ == "__main__":
    verify()
