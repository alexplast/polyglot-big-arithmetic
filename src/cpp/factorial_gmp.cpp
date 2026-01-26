#include <iostream>
#include <gmpxx.h>
#include <cstdlib>
#include <chrono>

int main() {
    const char* count_env = std::getenv("COUNT");
    int count = 200;
    if (count_env) count = std::atoi(count_env);

    mpz_class fact = 1;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 1; i <= count; ++i) {
        fact *= i;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result(" << count << "!): " << fact.get_str() << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
