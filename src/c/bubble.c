#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

int main() {
    int N = 10000;
    char *n_env = getenv("SORT_SIZE");
    if (n_env) N = atoi(n_env);

    double *arr = (double*)malloc(N * sizeof(double));
    
    // LCG Generator
    uint32_t seed = 42;
    for (int i = 0; i < N; i++) {
        seed = (seed * 1664525 + 1013904223);
        arr[i] = (double)seed / 4294967296.0;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    // Bubble Sort
    for (int i = 0; i < N - 1; i++) {
        for (int j = 0; j < N - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                double temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Sort(%d): ", N);
    // Print verify check (first 5 and last 5)
    for(int i=0; i<5; i++) printf("%.4f ", arr[i]);
    printf("... ");
    for(int i=N-5; i<N; i++) printf("%.4f ", arr[i]);
    printf("\n");
    
    printf("Time: %.3f ms\n", time_ms);
    free(arr);
    return 0;
}
