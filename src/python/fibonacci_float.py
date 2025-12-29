import os
import time

def main():
    try:
        count = int(os.environ.get("COUNT", 1475))
    except (ValueError, TypeError):
        count = 1475

    a, b = 0.0, 1.0
    start = time.perf_counter()
    for _ in range(count):
        a, b = b, a + b
    end = time.perf_counter()
    
    print(f"Result(F_{count}): {a:.10e}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
