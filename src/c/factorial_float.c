#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    char *count_env = getenv("COUNT");
    int count = 170;
    if (count_env) count = atoi(count_env);

    double factorial = 1.0;

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 1; i <= count; i++) {
        factorial *= (double)i;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Result(%d!): %.10e\n", count, factorial);
    printf("Time: %.6f ms\n", time_ms);
    return 0;
}
