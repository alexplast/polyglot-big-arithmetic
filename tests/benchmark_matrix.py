import subprocess
import os
import sys
import re

def run_command(cmd, n_size):
    env = os.environ.copy()
    env["MATRIX_SIZE"] = str(n_size)
    try:
        # Capture stderr to see why it fails
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
        
        # Check return code
        if result.returncode != 0:
            return None, f"Error (code {result.returncode})"

        match = re.search(r"Time: ([0-9\.\-eE]+) ms", result.stdout)
        if match:
            return float(match.group(1)), None
        return None, "Regex mismatch"
    except Exception as e:
        return None, str(e)

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
    except Exception as e:
        print(f"[ERROR] {e}")

def benchmark_matrix():
    N = 256
    print(f"--- Running Matrix Benchmark (N={N}) ---")
    
    languages = [
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
        print(f"Benchmarking {lang['name']}...", end="", flush=True)
        time_ms, error = run_command(lang['cmd'], N)
        
        if time_ms is not None:
             print(f" {time_ms:.3f} ms")
             results.append((lang['name'], time_ms))
        else:
             print(f" Failed ({error})")
             results.append((lang['name'], None))

    # Sort by time (fastest first), None at end
    results.sort(key=lambda x: x[1] if x[1] is not None else 99999999)

    # Get fastest time for ratio calculation
    fastest_time = None
    for r in results:
        if r[1] is not None:
            fastest_time = r[1]
            break

    md = f"| Language | Matrix Mult ({N}x{N}) | Relative Speed |\n"
    md += "| :--- | :--- | :--- |\n"
    
    for name, t in results:
        t_str = f"{t:.3f} ms" if t is not None else "FAILED"
        if t is not None and fastest_time is not None:
            if t == fastest_time:
                rel = "1.00x (Baseline)"
            else:
                rel = f"{t / fastest_time:.2f}x"
        else:
            rel = "-"
        
        md += f"| **{name}** | {t_str} | {rel} |\n"

    update_readme_section(md, "<!-- BENCHMARK_MATRIX_START -->", "<!-- BENCHMARK_MATRIX_END -->")

if __name__ == "__main__":
    benchmark_matrix()
