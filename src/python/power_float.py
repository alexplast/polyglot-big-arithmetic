import os
import time
import math

def main():
    try:
        base = float(os.environ.get("BASE", 2.0))
    except ValueError:
        base = 2.0
    
    try:
        exp = int(os.environ.get("EXP", 1023))
    except ValueError:
        exp = 1023

    start = time.perf_counter()
    result = math.pow(base, exp)
    end = time.perf_counter()
    
    print(f"Result({base}^{exp}): {result:.10e}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
