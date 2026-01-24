import os
import time
import struct
import sys

def main():
    try:
        N = int(os.environ.get("SORT_SIZE", 10000))
    except:
        N = 10000

    filename = "data.bin"
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found. Run 'python3 tests/gen_data.py' first.", file=sys.stderr)
        sys.exit(1)

    with open(filename, "rb") as f:
        data = f.read(N * 8)
        
    # unpack requires exact bytes for the format string
    # Calculate how many doubles we actually read
    actual_n = len(data) // 8
    if actual_n < N:
        print(f"Warning: requested {N}, but file only has {actual_n}", file=sys.stderr)
        # Pad with zeros or adjust N? 
        # For Bubble Sort consistency, let's just use what we have or fill.
        # Here we adjust list to be N size, filling rest with 0.0
        floats = list(struct.unpack(f'<{actual_n}d', data))
        arr = floats + [0.0] * (N - actual_n)
    else:
        arr = list(struct.unpack(f'<{N}d', data))

    start = time.perf_counter()
    
    # Pure Python Bubble Sort
    for i in range(N - 1):
        for j in range(N - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    end = time.perf_counter()

    print(f"Sort({N}): ", end="")
    p_limit = 5 if N >= 5 else N
    for i in range(p_limit): print(f"{arr[i]:.4f} ", end="")
    print("... ", end="")
    if N > 5:
        for i in range(N-5, N): print(f"{arr[i]:.4f} ", end="")
    print()
    
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
