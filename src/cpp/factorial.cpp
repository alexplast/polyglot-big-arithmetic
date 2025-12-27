#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <cstdlib>

struct BigInt {
    std::vector<int> digits; // stored in reverse order (0-indexed is 10^0)

    BigInt(long long n) {
        if (n == 0) digits.push_back(0);
        while (n > 0) {
            digits.push_back(n % 10);
            n /= 10;
        }
    }

    void multiply(int n) {
        int carry = 0;
        for (size_t i = 0; i < digits.size(); ++i) {
            long long current = (long long)digits[i] * n + carry;
            digits[i] = current % 10;
            carry = current / 10;
        }
        while (carry) {
            digits.push_back(carry % 10);
            carry /= 10;
        }
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

int main() {
    const char* count_env = std::getenv("COUNT");
    int count = 200;
    if (count_env) {
        count = std::atoi(count_env);
    }

    BigInt factorial(1);
    for (int i = 2; i <= count; ++i) {
        factorial.multiply(i);
    }

    std::cout << "Result(" << count << "!): " << factorial.toString() << std::endl;

    return 0;
}
