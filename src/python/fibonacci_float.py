import os
import time

def main():
    try:
        count = int(os.environ.get("COUNT", 1475))
    except:
        count = 1475

    a, b = 0.0, 1.0
    start = time.perf_counter()
    
    # Python is slow, reducing iterations to 20,000 for sanity (10x less than others)
    # We will adjust displayed time in benchmark script if needed, 
    # but let's keep it honest: Python is just slow.
    for _ in range(200000):
        a, b = 0.0, 1.0
        for _ in range(count):
            a, b = b, a + b
            
    end = time.perf_counter()
    
    print(f"Result: {a}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
