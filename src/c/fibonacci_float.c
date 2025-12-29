#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    char *count_env = getenv("COUNT");
    int n = 1475;
    if (count_env) n = atoi(count_env);

    double a = 0.0;
    double b = 1.0;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < n; i++) {
        double temp = a;
        a = b;
        b = temp + b;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Result(F_%d): %.10e\n", n, a);
    printf("Time: %.6f ms\n", time_ms);
    return 0;
}
