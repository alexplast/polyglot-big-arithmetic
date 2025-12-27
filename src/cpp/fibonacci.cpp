#include <iostream>
#include <cstdlib> // For getenv
#include <string>  // For stoll
#include <limits>  // For numeric_limits

int main() {
    int n = 10; // Default value for count
    const char* count_str = std::getenv("COUNT");
    if (count_str) {
        try {
            n = std::stoi(count_str);
        } catch (const std::exception& e) {
            std::cerr << "Error converting COUNT environment variable: " << e.what() << std::endl;
        }
    }

    unsigned long long a = 0, b = 1;
    std::cout << "Fibonacci Sequence (first " << n << " numbers):" << std::endl;
    for (int i = 0; i < n; i++) {
        if (a > std::numeric_limits<unsigned long long>::max() - b) {
            std::cerr << "\nError: Fibonacci sequence exceeds the unsigned long long limit." << std::endl;
            return 1;
        }
        std::cout << a << " ";
        unsigned long long temp = a;
        a = b;
        b = temp + b;
    }
    std::cout << std::endl; // New line after sequence
    return 0;
}
