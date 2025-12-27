import os
import sys
import time

# Increase limit for integer to string conversion
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(1000000)

def main():
    try:
        base = int(os.environ.get("BASE", 2))
    except ValueError:
        base = 2
    
    try:
        exp = int(os.environ.get("EXP", 1000))
    except ValueError:
        exp = 1000

    start = time.perf_counter()
    result = pow(base, exp)
    end = time.perf_counter()
    
    print(f"Result({base}^{exp}): {result}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
