#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

#define BASE 1000000000

typedef struct {
    uint64_t *digits;
    int size;
    int capacity;
} BigInt;

void init(BigInt *n, uint64_t val) {
    n->capacity = 1000; // Pre-allocate more for factorial
    n->digits = (uint64_t*)malloc(n->capacity * sizeof(uint64_t));
    n->digits[0] = val;
    n->size = 1;
}

void mul(BigInt *n, int val) {
    uint64_t carry = 0;
    for (int i = 0; i < n->size; i++) {
        uint64_t current = n->digits[i] * val + carry;
        n->digits[i] = current % BASE;
        carry = current / BASE;
    }
    while (carry) {
        if (n->size == n->capacity) {
            n->capacity *= 2;
            n->digits = (uint64_t*)realloc(n->digits, n->capacity * sizeof(uint64_t));
        }
        n->digits[n->size++] = carry % BASE;
        carry /= BASE;
    }
}

void print_bigint(BigInt *n) {
    if (n->size == 0) { printf("0"); return; }
    printf("%lu", n->digits[n->size - 1]);
    for (int i = n->size - 2; i >= 0; i--) {
        printf("%09lu", n->digits[i]);
    }
}

int main() {
    char *count_env = getenv("COUNT");
    int count = 200;
    if (count_env) count = atoi(count_env);

    BigInt fact;
    init(&fact, 1);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 2; i <= count; i++) {
        mul(&fact, i);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Result(%d!): ", count);
    print_bigint(&fact);
    printf("\nTime: %.3f ms\n", time_ms);

    free(fact.digits);
    return 0;
}
