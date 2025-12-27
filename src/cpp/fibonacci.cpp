#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdlib>

struct BigInt {
    std::vector<int> digits;

    BigInt(long long n = 0) {
        if (n == 0) digits.push_back(0);
        while (n > 0) {
            digits.push_back(n % 10);
            n /= 10;
        }
    }

    void add(const BigInt& other) {
        int carry = 0;
        size_t n = std::max(digits.size(), other.digits.size());
        for (size_t i = 0; i < n || carry; ++i) {
            if (i == digits.size()) digits.push_back(0);
            int d2 = i < other.digits.size() ? other.digits[i] : 0;
            int sum = digits[i] + d2 + carry;
            digits[i] = sum % 10;
            carry = sum / 10;
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

    for (int i = 0; i < n; i++) {
        BigInt temp = a;
        a = b;
        b.add(temp);
    }
    std::cout << "Result(F_" << n << "): " << a.toString() << std::endl;

    return 0;
}
