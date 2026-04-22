import math
import os
import re
import subprocess
import sys


def expected_result_zero(size):
    values_a = [1.0 + (index % 100) * 0.01 for index in range(size * size)]
    values_b = [1.0 - (index % 100) * 0.01 for index in range(size * size)]
    total = 0.0
    for k in range(size):
        total += values_a[k] * values_b[k * size]
    return total


def run_command(cmd, env_vars):
    executable = cmd.split()[0]
    if executable.startswith("./") and not os.path.exists(executable):
        return None

    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
    except Exception:
        return None

    if result.returncode != 0:
        return None
    return result.stdout.strip()


def parse_result_zero(output):
    if not output:
        return None

    match = re.search(r"Result\[0\]:\s*([-+0-9.eE]+)", output)
    if match:
        return float(match.group(1))
    return None


def verify():
    size = 32
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    expected = expected_result_zero(size)
    env = {"MATRIX_SIZE": str(size)}
    languages = [
        {"name": "Assembler", "cmd": "./bin/matrix/matrix_asm", "optional": True},
        {"name": "C", "cmd": "./bin/matrix/matrix_c"},
        {"name": "C++", "cmd": "./bin/matrix/matrix_cpp"},
        {"name": "Go", "cmd": "./bin/matrix/matrix_go"},
        {"name": "Rust", "cmd": "./bin/matrix/matrix_rs"},
        {"name": "Java", "cmd": "java -cp bin/matrix Matrix"},
        {"name": "Fortran", "cmd": "./bin/matrix/matrix_f90"},
        {"name": "Python", "cmd": "python3 src/python/matrix.py"},
        {"name": "JavaScript", "cmd": "node src/js/matrix.js"},
    ]

    print(f"--- Verifying Matrix Multiplication at {size}x{size} ---")

    all_passed = True
    for lang in languages:
        output = run_command(lang["cmd"], env)
        if output is None and lang.get("optional"):
            print(f"[{lang['name']}] SKIPPED (not built for this platform)")
            continue

        value = parse_result_zero(output)
        status = "PASSED" if value is not None and math.isclose(value, expected, rel_tol=0.0, abs_tol=1e-3) else "FAILED"

        if status == "FAILED":
            all_passed = False
            print(f"[{lang['name']}] {status}")
        else:
            print(f"[{lang['name']}] {status} (Result[0]={value:.4f})")

    if all_passed:
        print("\nAll matrix implementations verified correctly!")
    else:
        print("\nSome matrix verifications failed.")
        sys.exit(1)


if __name__ == "__main__":
    verify()
