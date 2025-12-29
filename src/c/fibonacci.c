#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>

#define BASE 1000000000

typedef struct {
    uint64_t *digits;
    int size;
    int capacity;
} BigInt;

void init(BigInt *n, uint64_t val) {
    n->capacity = 16;
    n->digits = (uint64_t*)malloc(n->capacity * sizeof(uint64_t));
    n->digits[0] = val;
    n->size = 1;
}

void free_bigint(BigInt *n) {
    free(n->digits);
}

void copy(BigInt *dest, BigInt *src) {
    if (dest->capacity < src->size) {
        dest->capacity = src->size + 16;
        dest->digits = (uint64_t*)realloc(dest->digits, dest->capacity * sizeof(uint64_t));
    }
    memcpy(dest->digits, src->digits, src->size * sizeof(uint64_t));
    dest->size = src->size;
}

void add(BigInt *dest, BigInt *other) {
    uint64_t carry = 0;
    int max_len = (dest->size > other->size) ? dest->size : other->size;
    
    if (dest->capacity <= max_len) {
        dest->capacity = max_len * 2;
        dest->digits = (uint64_t*)realloc(dest->digits, dest->capacity * sizeof(uint64_t));
    }

    for (int i = 0; i < max_len || carry; i++) {
        if (i == dest->size) {
            dest->digits[dest->size++] = 0;
        }
        
        uint64_t d2 = (i < other->size) ? other->digits[i] : 0;
        uint64_t sum = dest->digits[i] + d2 + carry;
        dest->digits[i] = sum % BASE;
        carry = sum / BASE;
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
    int count = 10;
    if (count_env) count = atoi(count_env);

    if (count == 0) { printf("Result(F_0): 0\n"); return 0; }

    BigInt a, b, temp;
    init(&a, 0);
    init(&b, 1);
    init(&temp, 0);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < count; i++) {
        copy(&temp, &a);
        copy(&a, &b);
        add(&b, &temp);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Result(F_%d): ", count);
    print_bigint(&a);
    printf("\nTime: %.3f ms\n", time_ms);

    free_bigint(&a);
    free_bigint(&b);
    free_bigint(&temp);
    return 0;
}
