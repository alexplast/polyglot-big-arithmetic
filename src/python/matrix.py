import os
import time

def main():
    try:
        N = int(os.environ.get("MATRIX_SIZE", 256))
    except:
        N = 256

    # Using pure lists to test interpreter speed
    A = [1.0 + (i % 100) * 0.01 for i in range(N * N)]
    B = [1.0 - (i % 100) * 0.01 for i in range(N * N)]
    C = [0.0] * (N * N)

    start = time.perf_counter()

    for i in range(N):
        for k in range(N):
            r = A[i * N + k]
            row_c_start = i * N
            row_b_start = k * N
            for j in range(N):
                C[row_c_start + j] += r * B[row_b_start + j]

    end = time.perf_counter()

    print(f"Matrix({N}x{N})")
    print(f"Result[0]: {C[0]}")
    print(f"Time: {(end - start) * 1000:.3f} ms")

if __name__ == "__main__":
    main()
