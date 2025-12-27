# Makefile for compiling Fibonacci and Factorial applications

COUNT ?= 10

# Default target: build all applications
all: bin_dirs cpp go rust java fortran

bin_dirs:
	@mkdir -p bin/fibo bin/fact

# C++
cpp: src/cpp/fibonacci.cpp src/cpp/factorial.cpp
	-g++ src/cpp/fibonacci.cpp -o bin/fibo/fibonacci_cpp
	-g++ src/cpp/factorial.cpp -o bin/fact/factorial_cpp

# Go
go: src/go/fibonacci.go src/go/factorial.go
	-go build -o bin/fibo/fibonacci_go src/go/fibonacci.go
	-go build -o bin/fact/factorial_go src/go/factorial.go

# Rust
rust: src/rust/fibonacci.rs src/rust/factorial.rs
	-rustc src/rust/fibonacci.rs -o bin/fibo/fibonacci_rs
	-rustc src/rust/factorial.rs -o bin/fact/factorial_rs

# Java
java: src/java/Fibonacci.java src/java/Factorial.java
	-javac -d bin/fibo src/java/Fibonacci.java
	-javac -d bin/fact src/java/Factorial.java

# Fortran
fortran: src/fortran/fibonacci.f90 src/fortran/factorial.f90
	-gfortran src/fortran/fibonacci.f90 -o bin/fibo/fibonacci_f90
	-gfortran src/fortran/factorial.f90 -o bin/fact/factorial_f90

# Phony targets
.PHONY: python js
python:
	@echo "Python is interpreted."

js:
	@echo "JavaScript is interpreted."

# Run Fibonacci
run: all
	@echo "--- Fibonacci (COUNT=$(COUNT)) ---"
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_cpp
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_go
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_rs
	-@env COUNT=$(COUNT) java -cp bin/fibo Fibonacci
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_f90
	-@env COUNT=$(COUNT) python3 src/python/fibonacci.py
	-@env COUNT=$(COUNT) node src/js/fibonacci.js

# Run Factorial
run_factorial: all
	@echo "--- Factorial (COUNT=$(COUNT)) ---"
	@echo "\n[C++]"
	-@env COUNT=$(COUNT) ./bin/fact/factorial_cpp
	@echo "\n[Go]"
	-@env COUNT=$(COUNT) ./bin/fact/factorial_go
	@echo "\n[Rust]"
	-@env COUNT=$(COUNT) ./bin/fact/factorial_rs
	@echo "\n[Java]"
	-@env COUNT=$(COUNT) java -cp bin/fact Factorial
	@echo "\n[Fortran]"
	-@env COUNT=$(COUNT) ./bin/fact/factorial_f90
	@echo "\n[Python]"
	-@env COUNT=$(COUNT) python3 src/python/factorial.py
	@echo "\n[JavaScript]"
	-@env COUNT=$(COUNT) node src/js/factorial.js

# Verify Factorial
verify_fact: all
	@python3 tests/verify_factorial.py $(COUNT)

# Verify Fibonacci
verify_fibo: all
	@python3 tests/verify_fibonacci.py $(COUNT)

# Verify All
verify_all: verify_fact verify_fibo

# Clean up compiled files
clean:
	rm -rf bin

