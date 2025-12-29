#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    char *n_env = getenv("MATRIX_SIZE");
    int N = 256;
    if (n_env) N = atoi(n_env);

    // Using 1D flat arrays
    double *A = (double*)malloc(N * N * sizeof(double));
    double *B = (double*)malloc(N * N * sizeof(double));
    double *C = (double*)calloc(N * N, sizeof(double));

    for(int i=0; i<N*N; ++i) {
        A[i] = 1.0 + (i % 100) * 0.01;
        B[i] = 1.0 - (i % 100) * 0.01;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < N; ++i) {
        for (int k = 0; k < N; ++k) {
            double r = A[i * N + k];
            for (int j = 0; j < N; ++j) {
                C[i * N + j] += r * B[k * N + j];
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Matrix(%dx%d)\n", N, N);
    printf("Result[0]: %.4f\n", C[0]);
    printf("Time: %.3f ms\n", time_ms);

    free(A); free(B); free(C);
    return 0;
}
