#!/usr/bin/env python3
import argparse
import csv
import json
import os
import platform
import re
import shlex
import statistics
import subprocess
import time

DEFAULT_RESULTS_DIR = "results"
DEFAULT_REPORT_FILE = "RESULTS.md"
DEFAULT_DATA_SEED = 1337

FULL_DEFAULTS = {
    "bigint": {"fib": "25000", "fact": "5000", "base": "2", "exp": "20000"},
    "float": {"count": "1475"},
    "matrix": {"size": "200"},
    "sort": {"size": "3000"},
}

SMOKE_DEFAULTS = {
    "bigint": {"fib": "5000", "fact": "1000", "base": "2", "exp": "5000"},
    "float": {"count": "256"},
    "matrix": {"size": "64"},
    "sort": {"size": "400"},
}

LANGS = {
    "asm": {"name": "Assembler", "type": "Native"},
    "c": {"name": "C", "type": "Custom Base 10^9"},
    "cpp": {"name": "C++", "type": "Custom Base 10^9"},
    "cpp_gmp": {"name": "C++ (GMP)", "type": "GMP Lib"},
    "rust": {"name": "Rust", "type": "Custom Base 10^9"},
    "rust_lib": {"name": "Rust (Lib)", "type": "num-bigint"},
    "go": {"name": "Go", "type": "math/big"},
    "java": {"name": "Java", "type": "BigInteger"},
    "js": {"name": "JavaScript", "type": "BigInt"},
    "python": {"name": "Python", "type": "Native"},
    "fortran": {"name": "Fortran", "type": "Custom Base 10^9"},
}


def bin_cmd(folder, name, ext=""):
    return f"./bin/{folder}/{name}_{ext}"


def java_cmd(folder, class_name):
    return f"java -cp bin/{folder} {class_name}"


def py_cmd(script):
    return f"python3 src/python/{script}"


def js_cmd(script):
    return f"node src/js/{script}"


def build_defaults(profile):
    source = FULL_DEFAULTS if profile == "full" else SMOKE_DEFAULTS
    return {key: value.copy() for key, value in source.items()}


def parse_time(stdout):
    match = re.search(r"Time: ([0-9.\-eE]+) ms", stdout)
    if match:
        return float(match.group(1))
    return None


def command_label(cmd):
    try:
        parts = shlex.split(cmd)
    except ValueError:
        return cmd
    if not parts:
        return cmd
    
    # Determine language based on command prefix or file extension
    lang = "Unknown"
    if parts[0] == "java":
        lang = "Java"
    elif parts[0] in ("python", "python3"):
        lang = "Python"
    elif parts[0] == "node":
        lang = "JavaScript"
    elif "rustc" in parts[0] or "cargo" in parts[0]:
        lang = "Rust"
    elif "gfortran" in parts[0]:
        lang = "Fortran"
    elif "gcc" in parts[0]:
        lang = "C"
    elif "g++" in parts[0]:
        lang = "C++"
    elif "bin/" in cmd:
        # Fallback for precompiled binaries: extract folder as language
        match = re.search(r"bin/([^/]+)/", cmd)
        if match:
            lang = match.group(1).capitalize()

    # Extract task name (e.g., 'fibonacci', 'factorial')
    task = "Task"
    for part in parts:
        if any(x in part for x in ("fibo", "fact", "power", "matrix", "bubble")):
            task = part.split('/')[-1].split('_')[0].capitalize()
            break

    return f"{lang}: {task}"


def run_once(cmd, env_vars):
    executable = cmd.split()[0]
    if executable.startswith("./") and not os.path.exists(executable):
        return None

    env = os.environ.copy()
    env.update(env_vars)
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, shell=True)
    except Exception as exc:
        print(f"\n[EXCEPTION] Error running {cmd}: {exc}")
        return None

    if result.returncode != 0:
        if result.returncode in (132, 139):
            return None
        if "Error:" in result.stdout or "Error:" in result.stderr:
            return None
        print(f"\n[ERROR] Command failed: {cmd}")
        return None

    return parse_time(result.stdout)


def summarize_times(times):
    return {
        "median": statistics.median(times),
        "min": min(times),
        "max": max(times),
        "stddev": statistics.stdev(times) if len(times) > 1 else 0.0,
    }


def run_benchmark_cmd(cmd, env_vars, runs, warmup):
    print(f"Running {command_label(cmd)}...", end=" ", flush=True)

    for _ in range(warmup):
        if run_once(cmd, env_vars) is None:
            print("[SKIP]", end=" ")
            return None

    times = []
    for _ in range(runs):
        sample = run_once(cmd, env_vars)
        if sample is None:
            print("[SKIP]", end=" ")
            return None
        times.append(sample)

    stats = summarize_times(times)
    print(f"OK ({stats['median']:.2f} ms)")
    return stats


def format_time(value):
    if value is None:
        return "—"
    return f"{value:.3f} ms"


def run_capture(command):
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True,
            check=False,
        )
    except Exception:
        return "Unavailable"

    output = (result.stdout or result.stderr).strip()
    if not output:
        return "Unavailable"
    return output.splitlines()[0]


def git_capture(args):
    repo_dir = os.getcwd()
    return run_capture(f"git -c safe.directory='{repo_dir}' {args}")


def detect_cpu():
    system = platform.system()
    if system == "Linux":
        if os.path.exists("/proc/cpuinfo"):
            with open("/proc/cpuinfo", "r", encoding="utf-8", errors="ignore") as handle:
                for line in handle:
                    if line.lower().startswith("model name"):
                        return line.split(":", 1)[1].strip()
        return run_capture("lscpu | grep 'Model name'")

    if system == "Darwin":
        return run_capture("sysctl -n machdep.cpu.brand_string")

    return platform.processor() or "Unavailable"


def detect_memory():
    system = platform.system()
    if system == "Linux" and os.path.exists("/proc/meminfo"):
        with open("/proc/meminfo", "r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                if line.startswith("MemTotal:"):
                    return line.split(":", 1)[1].strip()

    if system == "Darwin":
        raw = run_capture("sysctl -n hw.memsize")
        try:
            bytes_total = int(raw)
            gib = bytes_total / (1024 ** 3)
            return f"{gib:.1f} GiB"
        except ValueError:
            return raw

    return "Unavailable"


def collect_meta(args, defaults):
    data_seed = int(os.environ.get("DATA_SEED", str(DEFAULT_DATA_SEED)))
    return {
        "generated_on": time.strftime("%Y-%m-%d %H:%M:%S"),
        "host": {
            "platform": platform.platform(),
            "system": platform.system(),
            "machine": platform.machine(),
            "kernel": run_capture("uname -a"),
            "cpu": detect_cpu(),
            "memory": detect_memory(),
        },
        "git": {
            "commit": git_capture("rev-parse --short HEAD"),
            "branch": git_capture("branch --show-current"),
        },
        "tools": {
            "gcc": run_capture("gcc --version"),
            "g++": run_capture("g++ --version"),
            "gfortran": run_capture("gfortran --version"),
            "rustc": run_capture("rustc --version"),
            "cargo": run_capture("cargo --version"),
            "go": run_capture("go version"),
            "javac": run_capture("javac -version"),
            "python3": run_capture("python3 --version"),
            "node": run_capture("node --version"),
        },
        "run": {
            "bench": args.bench,
            "profile": args.profile,
            "runs": args.runs,
            "warmup": args.warmup,
            "plots": not args.no_plots,
            "report": not args.no_report,
            "results_dir": args.results_dir,
            "report_file": args.report_file,
            "data_seed": data_seed,
            "cases": {
                "bigint": defaults["bigint"],
                "float": defaults["float"],
                "matrix": defaults["matrix"],
                "sort": defaults["sort"],
            },
        },
    }


def write_meta(meta, path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2)


def render_meta_section(meta):
    tools = meta["tools"]
    run_cfg = meta["run"]
    cases = run_cfg["cases"]
    lines = [
        "## Environment & Run Settings",
        "",
        f"- Generated on: {meta['generated_on']}",
        f"- Git: branch `{meta['git']['branch']}`, commit `{meta['git']['commit']}`",
        f"- Host: {meta['host']['platform']}",
        f"- CPU: {meta['host']['cpu']}",
        f"- Memory: {meta['host']['memory']}",
        f"- Toolchain: gcc `{tools['gcc']}`; g++ `{tools['g++']}`; gfortran `{tools['gfortran']}`; rustc `{tools['rustc']}`; go `{tools['go']}`; javac `{tools['javac']}`; python `{tools['python3']}`; node `{tools['node']}`",
        f"- Run config: bench `{run_cfg['bench']}`, profile `{run_cfg['profile']}`, runs `{run_cfg['runs']}`, warmup `{run_cfg['warmup']}`, data seed `{run_cfg['data_seed']}`",
        f"- Problem sizes: factorial `{cases['bigint']['fact']}`, fibonacci `{cases['bigint']['fib']}`, power `{cases['bigint']['base']}^{cases['bigint']['exp']}`, float count `{cases['float']['count']}`, matrix `{cases['matrix']['size']}`, sort `{cases['sort']['size']}`",
        "",
        "---",
        "",
    ]
    return "\n".join(lines)


def init_report(report_file, meta):
    with open(report_file, "w", encoding="utf-8") as handle:
        handle.write("# Polyglot Benchmark Results\n\n")
        handle.write(f"Generated on: {meta['generated_on']}\n\n")
        handle.write(render_meta_section(meta))


def append_report_section(report_file, title, markdown_table, image_filename, image_prefix):
    print(f"\n--- {title} Results ---")
    print(markdown_table)

    with open(report_file, "a", encoding="utf-8") as handle:
        handle.write(f"## {title}\n\n")
        handle.write(markdown_table + "\n\n")
        if image_filename:
            handle.write(f"![{title} Graph]({image_prefix}/{image_filename})\n\n")
        handle.write("---\n\n")


def print_console_section(title, markdown_table):
    print(f"\n--- {title} Results ---")
    print(markdown_table)


def relative_speed(value, baseline):
    if value is None or baseline in (None, 0):
        return "—"
    if value == baseline:
        return "1.00x"
    return f"{value / baseline:.2f}x"


def csv_float(value):
    if value is None:
        return "0"
    return f"{value:.4f}"


def run_bigint(args, defaults, image_prefix):
    print(f"\n--- 1. BigInt Benchmark (Median of {args.runs} runs, warmup {args.warmup}) ---")
    targets = [
        ("C", bin_cmd("fibo", "fibonacci", "c"), bin_cmd("fact", "factorial", "c"), bin_cmd("power", "power", "c")),
        ("C++", bin_cmd("fibo", "fibonacci", "cpp"), bin_cmd("fact", "factorial", "cpp"), bin_cmd("power", "power", "cpp")),
        ("C++ (GMP)", bin_cmd("fibo", "fibonacci", "cpp_gmp"), bin_cmd("fact", "factorial", "cpp_gmp"), bin_cmd("power", "power", "cpp_gmp")),
        ("Rust", bin_cmd("fibo", "fibonacci", "rs"), bin_cmd("fact", "factorial", "rs"), bin_cmd("power", "power", "rs")),
        ("Rust (Lib)", bin_cmd("fibo", "fibonacci", "rs_lib"), bin_cmd("fact", "factorial", "rs_lib"), bin_cmd("power", "power", "rs_lib")),
        ("Go", bin_cmd("fibo", "fibonacci", "go"), bin_cmd("fact", "factorial", "go"), bin_cmd("power", "power", "go")),
        ("Java", java_cmd("fibo", "Fibonacci"), java_cmd("fact", "Factorial"), java_cmd("power", "Power")),
        ("Python", py_cmd("fibonacci.py"), py_cmd("factorial.py"), py_cmd("power.py")),
        ("JavaScript", js_cmd("fibonacci.js"), js_cmd("factorial.js"), js_cmd("power.js")),
        ("Fortran", bin_cmd("fibo", "fibonacci", "f90"), bin_cmd("fact", "factorial", "f90"), bin_cmd("power", "power", "f90")),
    ]

    env_fib = {"COUNT": defaults["bigint"]["fib"]}
    env_fact = {"COUNT": defaults["bigint"]["fact"]}
    env_pow = {"BASE": defaults["bigint"]["base"], "EXP": defaults["bigint"]["exp"]}
    results = []

    for name, cmd_fib, cmd_fact, cmd_pow in targets:
        fib = run_benchmark_cmd(cmd_fib, env_fib, args.runs, args.warmup)
        fact = run_benchmark_cmd(cmd_fact, env_fact, args.runs, args.warmup)
        power = run_benchmark_cmd(cmd_pow, env_pow, args.runs, args.warmup)
        impl_type = next((value["type"] for value in LANGS.values() if value["name"] == name), "Unknown")
        results.append({"name": name, "fib": fib, "fact": fact, "pow": power, "type": impl_type})

    results.sort(key=lambda item: item["fact"]["median"] if item["fact"] else float("inf"))
    baseline = next((item["fact"]["median"] for item in results if item["fact"]), None)

    csv_path = os.path.join(args.results_dir, "bigint_benchmark.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(
            [
                "Language",
                "Factorial Time (ms)",
                "Factorial Min (ms)",
                "Factorial Max (ms)",
                "Factorial StdDev (ms)",
                "Relative Speed",
                "Fibonacci Time (ms)",
                "Fibonacci Min (ms)",
                "Fibonacci Max (ms)",
                "Fibonacci StdDev (ms)",
                "Power Time (ms)",
                "Power Min (ms)",
                "Power Max (ms)",
                "Power StdDev (ms)",
                "Implementation Type",
            ]
        )
        for item in results:
            fact = item["fact"]
            fib = item["fib"]
            power = item["pow"]
            writer.writerow(
                [
                    item["name"],
                    csv_float(fact["median"] if fact else None),
                    csv_float(fact["min"] if fact else None),
                    csv_float(fact["max"] if fact else None),
                    csv_float(fact["stddev"] if fact else None),
                    relative_speed(fact["median"] if fact else None, baseline).replace("—", "0.00x"),
                    csv_float(fib["median"] if fib else None),
                    csv_float(fib["min"] if fib else None),
                    csv_float(fib["max"] if fib else None),
                    csv_float(fib["stddev"] if fib else None),
                    csv_float(power["median"] if power else None),
                    csv_float(power["min"] if power else None),
                    csv_float(power["max"] if power else None),
                    csv_float(power["stddev"] if power else None),
                    item["type"],
                ]
            )

    markdown = "| Language | Factorial | Rel Speed | Fibonacci | Power | Type |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    for item in results:
        fact = item["fact"]["median"] if item["fact"] else None
        fib = item["fib"]["median"] if item["fib"] else None
        power = item["pow"]["median"] if item["pow"] else None
        markdown += (
            f"| **{item['name']}** | {format_time(fact)} | {relative_speed(fact, baseline)} | "
            f"{format_time(fib)} | {format_time(power)} | {item['type']} |\n"
        )

    if args.no_report:
        print_console_section("BigInt Performance", markdown)
    else:
        append_report_section(args.report_file, "BigInt Performance", markdown, "bigint.png", image_prefix)


def run_generic_bench(args, key, title, cmd_map, env, csv_name, img_name, image_prefix):
    print(f"\n--- {title} ---")
    results = []
    for language, cmd in cmd_map.items():
        stats = run_benchmark_cmd(cmd, env, args.runs, args.warmup)
        results.append({"name": language, "stats": stats})

    results.sort(key=lambda item: item["stats"]["median"] if item["stats"] else float("inf"))
    baseline = next((item["stats"]["median"] for item in results if item["stats"]), None)

    key_str = f"{key} Time (ms)"
    if key == "Float":
        key_str = "Float Time (50k iter)"

    csv_path = os.path.join(args.results_dir, csv_name)
    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["Language", key_str, "Min Time (ms)", "Max Time (ms)", "StdDev (ms)", "Relative Speed"])
        for item in results:
            stats = item["stats"]
            value = stats["median"] if stats else None
            writer.writerow(
                [
                    item["name"],
                    csv_float(value),
                    csv_float(stats["min"] if stats else None),
                    csv_float(stats["max"] if stats else None),
                    csv_float(stats["stddev"] if stats else None),
                    relative_speed(value, baseline).replace("—", "0.00x"),
                ]
            )

    markdown = "| Language | Time | Rel Speed |\n| :--- | :--- | :--- |\n"
    for item in results:
        value = item["stats"]["median"] if item["stats"] else None
        markdown += f"| **{item['name']}** | {format_time(value)} | {relative_speed(value, baseline)} |\n"

    if args.no_report:
        print_console_section(title, markdown)
    else:
        append_report_section(args.report_file, title, markdown, img_name, image_prefix)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench", choices=["all", "bigint", "float", "matrix", "sort"], default="all")
    parser.add_argument("--profile", choices=["full", "smoke"], default="full")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument("--results-dir", default=DEFAULT_RESULTS_DIR)
    parser.add_argument("--report-file", default=DEFAULT_REPORT_FILE)
    parser.add_argument("--meta", default=None, help="Path to metadata JSON output")
    parser.add_argument("--no-plots", action="store_true")
    parser.add_argument("--no-report", action="store_true")
    args = parser.parse_args()

    defaults = build_defaults(args.profile)
    args.meta = args.meta or os.path.join(args.results_dir, "meta.json")
    os.makedirs(args.results_dir, exist_ok=True)

    meta = collect_meta(args, defaults)
    write_meta(meta, args.meta)

    image_prefix = f"{args.results_dir}/plots".replace("\\", "/")
    if not args.no_report:
        init_report(args.report_file, meta)

    if args.bench in ("all", "bigint"):
        run_bigint(args, defaults, image_prefix)

    if args.bench in ("all", "float"):
        targets = {
            "C": bin_cmd("float/fibo", "fibonacci", "c"),
            "C++": bin_cmd("float/fibo", "fibonacci", "cpp"),
            "Rust": bin_cmd("float/fibo", "fibonacci", "rs"),
            "Go": bin_cmd("float/fibo", "fibonacci", "go"),
            "Java": java_cmd("float/fibo", "FibonacciFloat"),
            "Python": py_cmd("fibonacci_float.py"),
            "JavaScript": js_cmd("fibonacci_float.js"),
            "Fortran": bin_cmd("float/fibo", "fibonacci", "f90"),
        }
        run_generic_bench(
            args,
            "Float",
            "Float Throughput",
            targets,
            {"COUNT": defaults["float"]["count"]},
            "float_benchmark.csv",
            "float.png",
            image_prefix,
        )

    if args.bench in ("all", "matrix"):
        targets = {
            "Assembler": bin_cmd("matrix", "matrix", "asm"),
            "C": bin_cmd("matrix", "matrix", "c"),
            "C++": bin_cmd("matrix", "matrix", "cpp"),
            "Rust": bin_cmd("matrix", "matrix", "rs"),
            "Fortran": bin_cmd("matrix", "matrix", "f90"),
            "Go": bin_cmd("matrix", "matrix", "go"),
            "Java": java_cmd("matrix", "Matrix"),
            "JavaScript": js_cmd("matrix.js"),
            "Python": py_cmd("matrix.py"),
        }
        run_generic_bench(
            args,
            "Matrix",
            "Matrix Multiplication",
            targets,
            {"MATRIX_SIZE": defaults["matrix"]["size"]},
            "matrix_benchmark.csv",
            "matrix.png",
            image_prefix,
        )

    if args.bench in ("all", "sort"):
        targets = {
            "Assembler": bin_cmd("sort", "bubble", "asm"),
            "C": bin_cmd("sort", "bubble", "c"),
            "C++": bin_cmd("sort", "bubble", "cpp"),
            "Rust": bin_cmd("sort", "bubble", "rs"),
            "Fortran": bin_cmd("sort", "bubble", "f90"),
            "Go": bin_cmd("sort", "bubble", "go"),
            "Java": java_cmd("sort", "Bubble"),
            "JavaScript": js_cmd("bubble.js"),
            "Python": py_cmd("bubble.py"),
        }
        run_generic_bench(
            args,
            "Sort",
            "Bubble Sort",
            targets,
            {"SORT_SIZE": defaults["sort"]["size"]},
            "sort_benchmark.csv",
            "sort.png",
            image_prefix,
        )

    if not args.no_plots:
        print("\n--- Generating Plots ---")
        subprocess.run(
            [
                "python3",
                "tests/plot.py",
                "--results-dir",
                args.results_dir,
            ],
            check=True,
        )

    target = args.report_file if not args.no_report else args.results_dir
    print(f"Done! Check {target}")


if __name__ == "__main__":
    main()
