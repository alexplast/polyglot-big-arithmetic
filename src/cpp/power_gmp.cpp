#include <iostream>
#include <gmpxx.h>
#include <cstdlib>
#include <chrono>

int main() {
    const char* base_env = std::getenv("BASE");
    const char* exp_env = std::getenv("EXP");
    
    unsigned long base = 2;
    unsigned long exp = 1000;
    
    if (base_env) base = std::strtoul(base_env, nullptr, 10);
    if (exp_env) exp = std::strtoul(exp_env, nullptr, 10);

    mpz_class result;
    mpz_class base_mpz = base;

    auto start = std::chrono::high_resolution_clock::now();
    // GMP has an optimized power function for unsigned long exponents
    mpz_pow_ui(result.get_mpz_t(), base_mpz.get_mpz_t(), exp);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result(" << base << "^" << exp << "): " << result.get_str() << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
