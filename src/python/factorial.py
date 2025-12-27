import os
import sys
import time

# Increase limit for integer to string conversion
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(1000000)

def main():
    try:
        count = int(os.environ.get("COUNT", 200))
    except ValueError:
        count = 200

    # print(f"Calculating Factorial({count})...")

    factorial = 1
    start = time.perf_counter()
    for i in range(1, count + 1):
        factorial *= i
    end = time.perf_counter()
    
    print(f"Result({count}!): {factorial}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
