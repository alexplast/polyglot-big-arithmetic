import os

def fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        print(a, end=" ")
        a, b = b, a + b

count = int(os.getenv("COUNT", 10))
print(f"Fibonacci Sequence (first {count} numbers):")
fibonacci(count)
