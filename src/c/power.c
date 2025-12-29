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
    n->digits = (uint64_t*)calloc(n->capacity, sizeof(uint64_t));
    if (val == 0) {
        n->size = 0; // Handle 0 specifically usually, but here we treat size 0 as 0
        n->digits[0] = 0;
        n->size = 1;
    } else {
        n->digits[0] = val;
        n->size = 1;
    }
    while (val >= BASE) { // Handle init with > BASE if needed
        n->digits[n->size-1] = val % BASE;
        val /= BASE;
        if (n->size == n->capacity) {
           n->capacity *= 2;
           n->digits = (uint64_t*)realloc(n->digits, n->capacity * sizeof(uint64_t));
        }
        n->digits[n->size++] = val;
    }
}

// Result = A * B
void multiply(BigInt *res, BigInt *a, BigInt *b) {
    // Reset result
    if (res->capacity < a->size + b->size) {
        res->capacity = a->size + b->size + 16;
        res->digits = (uint64_t*)realloc(res->digits, res->capacity * sizeof(uint64_t));
    }
    // Zero out
    memset(res->digits, 0, res->capacity * sizeof(uint64_t));
    
    for (int i = 0; i < a->size; i++) {
        uint64_t carry = 0;
        for (int j = 0; j < b->size || carry; j++) {
            uint64_t d2 = (j < b->size) ? b->digits[j] : 0;
            uint64_t current = res->digits[i + j] + (a->digits[i] * d2) + carry;
            res->digits[i + j] = current % BASE;
            carry = current / BASE;
        }
    }
    
    res->size = a->size + b->size;
    while (res->size > 1 && res->digits[res->size - 1] == 0) {
        res->size--;
    }
}

void copy(BigInt *dest, BigInt *src) {
    if (dest->capacity < src->size) {
        dest->capacity = src->size + 16;
        dest->digits = (uint64_t*)realloc(dest->digits, dest->capacity * sizeof(uint64_t));
    }
    memcpy(dest->digits, src->digits, src->size * sizeof(uint64_t));
    dest->size = src->size;
}

void print_bigint(BigInt *n) {
    if (n->size == 0) { printf("0"); return; }
    printf("%lu", n->digits[n->size - 1]);
    for (int i = n->size - 2; i >= 0; i--) {
        printf("%09lu", n->digits[i]);
    }
}

int main() {
    char *base_env = getenv("BASE");
    char *exp_env = getenv("EXP");
    int base_val = 2;
    int exp_val = 1000;
    if (base_env) base_val = atoi(base_env);
    if (exp_env) exp_val = atoi(exp_env);

    BigInt base, result, temp_base, temp_res;
    init(&base, base_val);
    init(&result, 1);
    init(&temp_base, 0); // buffers
    init(&temp_res, 0);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    while (exp_val > 0) {
        if (exp_val % 2 == 1) {
            multiply(&temp_res, &result, &base); // temp = res * base
            copy(&result, &temp_res);            // res = temp
        }
        multiply(&temp_base, &base, &base);      // temp = base * base
        copy(&base, &temp_base);                 // base = temp
        exp_val /= 2;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double time_ms = (end.tv_sec - start.tv_sec) * 1000.0 + (end.tv_nsec - start.tv_nsec) / 1000000.0;

    printf("Result(%d^%s): ", base_val, exp_env ? exp_env : "1000");
    print_bigint(&result);
    printf("\nTime: %.3f ms\n", time_ms);

    free(base.digits); free(result.digits);
    free(temp_base.digits); free(temp_res.digits);
    return 0;
}
