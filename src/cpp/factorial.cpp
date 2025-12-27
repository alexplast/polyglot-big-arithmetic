#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstdlib>
#include <chrono>
#include <iomanip>

// Optimized BigInt using Base 10^9
struct BigInt {
    static const int BASE = 1000000000;
    std::vector<int> digits; 

    BigInt(long long n) {
        if (n == 0) digits.push_back(0);
        while (n > 0) {
            digits.push_back(n % BASE);
            n /= BASE;
        }
    }

    void multiply(int n) {
        long long carry = 0;
        for (size_t i = 0; i < digits.size(); ++i) {
            long long current = (long long)digits[i] * n + carry;
            digits[i] = current % BASE;
            carry = current / BASE;
        }
        while (carry) {
            digits.push_back(carry % BASE);
            carry /= BASE;
        }
    }

    void print() const {
        if (digits.empty()) {
            std::cout << "0";
            return;
        }
        std::cout << digits.back();
        for (int i = digits.size() - 2; i >= 0; --i) {
            std::cout << std::setfill('0') << std::setw(9) << digits[i];
        }
    }
};

int main() {
    const char* count_env = std::getenv("COUNT");
    int count = 200;
    if (count_env) {
        count = std::atoi(count_env);
    }

    BigInt factorial(1);
    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 2; i <= count; ++i) {
        factorial.multiply(i);
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result(" << count << "!): ";
    factorial.print();
    std::cout << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
