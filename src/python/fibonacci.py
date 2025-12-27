import os
import sys
import time

# Increase limit for integer to string conversion
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(1000000)

def main():
    try:
        count = int(os.environ.get("COUNT", 10))
    except (ValueError, TypeError):
        count = 10

    if count < 0:
        return

    a, b = 0, 1
    start = time.perf_counter()
    for _ in range(count):
        a, b = b, a + b
    end = time.perf_counter()
    
    print(f"Result(F_{count}): {a}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
