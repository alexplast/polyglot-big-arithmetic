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

    BigInt(long long n = 1) {
        if (n == 0) digits.push_back(0);
        while (n > 0) {
            digits.push_back(n % BASE);
            n /= BASE;
        }
    }

    // Multiply by another BigInt
    BigInt multiply(const BigInt& other) const {
        if (digits.empty() || other.digits.empty()) return BigInt(0);
        
        std::vector<long long> result(digits.size() + other.digits.size(), 0);
        
        for (size_t i = 0; i < digits.size(); ++i) {
            long long carry = 0;
            for (size_t j = 0; j < other.digits.size() || carry; ++j) {
                long long d2 = j < other.digits.size() ? other.digits[j] : 0;
                long long current = result[i + j] + (long long)digits[i] * d2 + carry;
                result[i + j] = current % BASE;
                carry = current / BASE;
            }
        }
        
        // Remove leading zeros and convert back to int vector
        while (result.size() > 1 && result.back() == 0) {
            result.pop_back();
        }
        
        BigInt res;
        res.digits.resize(result.size());
        for(size_t i=0; i<result.size(); ++i) {
            res.digits[i] = (int)result[i];
        }
        return res;
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

// Binary exponentiation
BigInt power(BigInt base, int exp) {
    BigInt result(1);
    
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = result.multiply(base);
        }
        base = base.multiply(base);
        exp /= 2;
    }
    
    return result;
}

int main() {
    const char* base_env = std::getenv("BASE");
    const char* exp_env = std::getenv("EXP");
    
    int base = 2;
    int exp = 1000;
    
    if (base_env) {
        base = std::atoi(base_env);
    }
    if (exp_env) {
        exp = std::atoi(exp_env);
    }

    BigInt bigBase(base);
    
    auto start = std::chrono::high_resolution_clock::now();
    BigInt result = power(bigBase, exp);
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);

    std::cout << "Result(" << base << "^" << exp << "): ";
    result.print();
    std::cout << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
