#include <iostream>
#include <gmpxx.h>
#include <cstdlib>
#include <chrono>

int main() {
    const char* count_env = std::getenv("COUNT");
    int n = 10;
    if (count_env) n = std::atoi(count_env);

    mpz_class a = 0;
    mpz_class b = 1;

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; ++i) {
        mpz_class temp = a;
        a = b;
        b += temp;
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result(F_" << n << "): " << a.get_str() << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
