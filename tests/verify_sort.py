import math
import os
import random
import re
import subprocess
import sys


def expected_preview(size, seed):
    generator = random.Random(seed)
    values = [generator.random() for _ in range(size)]
    values.sort()
    head = [round(value, 4) for value in values[:5]]
    tail = [round(value, 4) for value in values[-5:]]
    return head + tail


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


def parse_preview(output):
    if not output:
        return None

    sort_line = None
    for line in output.splitlines():
        if line.startswith("Sort("):
            sort_line = line
            break

    if sort_line is None or ":" not in sort_line:
        return None

    preview = sort_line.split(":", 1)[1]
    matches = re.findall(r"[-+]?(?:\d+\.\d+|\.\d+)", preview)
    if len(matches) < 10:
        return None

    return [float(value) for value in matches[:10]]


def verify():
    size = 64
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    seed = int(os.environ.get("DATA_SEED", "1337"))
    expected = expected_preview(size, seed)
    env = {"SORT_SIZE": str(size)}
    languages = [
        {"name": "Assembler", "cmd": "./bin/sort/bubble_asm", "optional": True},
        {"name": "C", "cmd": "./bin/sort/bubble_c"},
        {"name": "C++", "cmd": "./bin/sort/bubble_cpp"},
        {"name": "Go", "cmd": "./bin/sort/bubble_go"},
        {"name": "Rust", "cmd": "./bin/sort/bubble_rs"},
        {"name": "Java", "cmd": "java -cp bin/sort Bubble"},
        {"name": "Fortran", "cmd": "./bin/sort/bubble_f90"},
        {"name": "Python", "cmd": "python3 src/python/bubble.py"},
        {"name": "JavaScript", "cmd": "node src/js/bubble.js"},
    ]

    print(f"--- Verifying Bubble Sort with {size} elements ---")

    all_passed = True
    for lang in languages:
        output = run_command(lang["cmd"], env)
        if output is None and lang.get("optional"):
            print(f"[{lang['name']}] SKIPPED (not built for this platform)")
            continue

        actual = parse_preview(output)
        status = "PASSED"
        if actual is None:
            status = "FAILED"
        else:
            for expected_value, actual_value in zip(expected, actual):
                if not math.isclose(actual_value, expected_value, rel_tol=0.0, abs_tol=1e-4):
                    status = "FAILED"
                    break

        if status == "FAILED":
            all_passed = False
            print(f"[{lang['name']}] {status}")
        else:
            print(f"[{lang['name']}] {status}")

    if all_passed:
        print("\nAll sort implementations verified correctly!")
    else:
        print("\nSome sort verifications failed.")
        sys.exit(1)


if __name__ == "__main__":
    verify()
