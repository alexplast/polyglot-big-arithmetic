#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstdlib>
#include <chrono>

struct BigInt {
    std::vector<int> digits; // stored in reverse order (0-indexed is 10^0)

    BigInt(long long n = 1) {
        if (n == 0) digits.push_back(0);
        while (n > 0) {
            digits.push_back(n % 10);
            n /= 10;
        }
    }

    // Multiply by another BigInt
    BigInt multiply(const BigInt& other) const {
        std::vector<int> result(digits.size() + other.digits.size(), 0);
        
        for (size_t i = 0; i < digits.size(); ++i) {
            int carry = 0;
            for (size_t j = 0; j < other.digits.size() || carry; ++j) {
                int d2 = j < other.digits.size() ? other.digits[j] : 0;
                long long current = result[i + j] + (long long)digits[i] * d2 + carry;
                result[i + j] = current % 10;
                carry = current / 10;
            }
        }
        
        // Remove leading zeros
        while (result.size() > 1 && result.back() == 0) {
            result.pop_back();
        }
        
        BigInt res;
        res.digits = result;
        return res;
    }

    std::string toString() const {
        if (digits.empty()) return "0";
        std::string s = "";
        for (int i = digits.size() - 1; i >= 0; --i) {
            s += (char)('0' + digits[i]);
        }
        return s;
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

    std::cout << "Result(" << base << "^" << exp << "): " << result.toString() << std::endl;
    std::cout << "Time: " << duration.count() / 1000.0 << " ms" << std::endl;

    return 0;
}
