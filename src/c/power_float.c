#include <stdio.h>
#include <stdlib.h>
#include <time.h>

double power(double base, int exp) {
    double result = 1.0;
    double b = base;
    while (exp > 0) {
        if (exp % 2 == 1) result *= b;
        b *= b;
        exp /= 2;
    }
    return result;
}

int main() {
    char *base_env = getenv("BASE");
    char *exp_env = getenv("EXP");
    double base = 2.0;
    int exp = 1023;
    if (base_env) base = atof(base_env);
    if (exp_env) exp = atoi(exp_env);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    double result = power(base, exp);

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Result(%.2f^%d): %.10e\n", base, exp, result);
    printf("Time: %.6f ms\n", time_ms);
    return 0;
}
