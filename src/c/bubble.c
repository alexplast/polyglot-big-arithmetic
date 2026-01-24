#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

int main() {
    int N = 10000;
    char *n_env = getenv("SORT_SIZE");
    if (n_env) N = atoi(n_env);

    double *arr = (double*)malloc(N * sizeof(double));
    if (!arr) { perror("malloc"); return 1; }

    // Read from binary file
    FILE *f = fopen("data.bin", "rb");
    if (!f) {
        fprintf(stderr, "Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first.\n");
        free(arr);
        return 1;
    }
    size_t read_count = fread(arr, sizeof(double), N, f);
    fclose(f);

    if (read_count < N) {
        fprintf(stderr, "Warning: File contained fewer elements (%lu) than requested (%d).\n", read_count, N);
        // We continue with what we read, or update N
        N = read_count;
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
    int print_limit = (N < 5) ? N : 5;
    for(int i=0; i<print_limit; i++) printf("%.4f ", arr[i]);
    printf("... ");
    if (N > 5) {
        for(int i=N-5; i<N; i++) printf("%.4f ", arr[i]);
    }
    printf("\n");
    
    printf("Time: %.3f ms\n", time_ms);
    free(arr);
    return 0;
}
