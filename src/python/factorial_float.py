import os
import time

def main():
    try:
        count = int(os.environ.get("COUNT", 170))
    except ValueError:
        count = 170

    factorial = 1.0
    start = time.perf_counter()
    for i in range(1, count + 1):
        factorial *= float(i)
    end = time.perf_counter()
    
    print(f"Result({count}!): {factorial:.10e}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
