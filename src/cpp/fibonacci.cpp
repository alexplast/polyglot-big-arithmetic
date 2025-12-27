#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>
#include <chrono>
#include <iomanip>

// Optimized BigInt using Base 10^9
struct BigInt {
    static const int BASE = 1000000000;
    std::vector<int> digits;

    BigInt(long long n = 0) {
        if (n == 0) digits.push_back(0);
        while (n > 0) {
            digits.push_back(n % BASE);
            n /= BASE;
        }
    }

    void add(const BigInt& other) {
        int carry = 0;
        size_t n = std::max(digits.size(), other.digits.size());
        for (size_t i = 0; i < n || carry; ++i) {
            if (i == digits.size()) digits.push_back(0);
            long long d2 = i < other.digits.size() ? other.digits[i] : 0;
            long long sum = (long long)digits[i] + d2 + carry;
            digits[i] = sum % BASE;
            carry = sum / BASE;
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
    int n = 10;
    if (count_env) {
        n = std::atoi(count_env);
    }

    if (n < 0) return 0;
    if (n == 0) {
        std::cout << "Result(F_0): 0" << std::endl;
        return 0;
    }

    BigInt a(0);
    BigInt b(1);

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < n; i++) {
        BigInt temp = a; // Copy
        a = b;           // Copy
        b.add(temp);     // In-place add
    }
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result(F_" << n << "): ";
    a.print();
    std::cout << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
