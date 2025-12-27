# Makefile for Fibonacci and Factorial project

COUNT ?= 10

# Default target: build everything
all: fibo fact

fibo: bin_dirs cpp_fibo go_fibo rust_fibo java_fibo fortran_fibo
fact: bin_dirs cpp_fact go_fact rust_fact java_fact fortran_fact

bin_dirs:
	@mkdir -p bin/fibo bin/fact

# C++
cpp_fibo: src/cpp/fibonacci.cpp
	-g++ src/cpp/fibonacci.cpp -o bin/fibo/fibonacci_cpp
cpp_fact: src/cpp/factorial.cpp
	-g++ src/cpp/factorial.cpp -o bin/fact/factorial_cpp

# Go
go_fibo: src/go/fibonacci.go
	-go build -o bin/fibo/fibonacci_go src/go/fibonacci.go
go_fact: src/go/factorial.go
	-go build -o bin/fact/factorial_go src/go/factorial.go

# Rust
rust_fibo: src/rust/fibonacci.rs
	-rustc src/rust/fibonacci.rs -o bin/fibo/fibonacci_rs
rust_fact: src/rust/factorial.rs
	-rustc src/rust/factorial.rs -o bin/fact/factorial_rs

# Java
java_fibo: src/java/Fibonacci.java
	-javac -d bin/fibo src/java/Fibonacci.java
java_fact: src/java/Factorial.java
	-javac -d bin/fact src/java/Factorial.java

# Fortran
fortran_fibo: src/fortran/fibonacci.f90
	-gfortran src/fortran/fibonacci.f90 -o bin/fibo/fibonacci_f90
fortran_fact: src/fortran/factorial.f90
	-gfortran src/fortran/factorial.f90 -o bin/fact/factorial_f90

# Phony targets
.PHONY: python js
python:
	@echo "Python is interpreted."

js:
	@echo "JavaScript is interpreted."

# Run Fibonacci
run: fibo
	@echo "--- Fibonacci (COUNT=$(COUNT)) ---"
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_cpp
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_go
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_rs
	-@env COUNT=$(COUNT) java -cp bin/fibo Fibonacci
	-@env COUNT=$(COUNT) ./bin/fibo/fibonacci_f90
	-@env COUNT=$(COUNT) python3 src/python/fibonacci.py
	-@env COUNT=$(COUNT) node src/js/fibonacci.js

# Run Factorial
run_factorial: fact
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

# Verify Fibonacci
verify_fibo: fibo
	@python3 tests/verify_fibonacci.py $(COUNT)

# Verify Factorial
verify_fact: fact
	@python3 tests/verify_factorial.py $(COUNT)

# Verify All
verify_all: verify_fibo verify_fact

# Clean up compiled files
clean:
	rm -rf bin

