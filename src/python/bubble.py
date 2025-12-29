import os
import time

def main():
    try:
        N = int(os.environ.get("SORT_SIZE", 10000))
    except:
        N = 10000

    arr = [0.0] * N
    seed = 42
    
    for i in range(N):
        seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
        arr[i] = float(seed) / 4294967296.0

    start = time.perf_counter()
    
    # Pure Python Bubble Sort
    # Using range(len) is standard
    for i in range(N - 1):
        for j in range(N - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    end = time.perf_counter()

    print(f"Sort({N}): ", end="")
    for i in range(5): print(f"{arr[i]:.4f} ", end="")
    print("... ", end="")
    for i in range(N-5, N): print(f"{arr[i]:.4f} ", end="")
    print()
    
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
