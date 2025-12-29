# Makefile for Fibonacci, Factorial and Power project (BigInt + Float)

COUNT ?= 10
BASE ?= 2
EXP ?= 1000

# Limits for Float benchmark
FLOAT_COUNT_FIBO ?= 1475
FLOAT_COUNT_FACT ?= 170
FLOAT_BASE ?= 2
FLOAT_EXP ?= 1023

# Default target: build everything (BigInt)
all: fibo fact power

# Build Float versions
float: bin_dirs float_compile

fibo: bin_dirs cpp_fibo go_fibo rust_fibo java_fibo fortran_fibo
fact: bin_dirs cpp_fact go_fact rust_fact java_fact fortran_fact
power: bin_dirs cpp_power go_power rust_power java_power fortran_power

bin_dirs:
	@mkdir -p bin/fibo bin/fact bin/power
	@mkdir -p bin/float/fibo bin/float/fact bin/float/power

# --- C++ ---
cpp_fibo: src/cpp/fibonacci.cpp
	-g++ src/cpp/fibonacci.cpp -o bin/fibo/fibonacci_cpp
cpp_fact: src/cpp/factorial.cpp
	-g++ src/cpp/factorial.cpp -o bin/fact/factorial_cpp
cpp_power: src/cpp/power.cpp
	-g++ src/cpp/power.cpp -o bin/power/power_cpp

# --- Go ---
go_fibo: src/go/fibonacci.go
	-go build -o bin/fibo/fibonacci_go src/go/fibonacci.go
go_fact: src/go/factorial.go
	-go build -o bin/fact/factorial_go src/go/factorial.go
go_power: src/go/power.go
	-go build -o bin/power/power_go src/go/power.go

# --- Rust ---
rust_fibo: src/rust/fibonacci.rs
	-rustc src/rust/fibonacci.rs -o bin/fibo/fibonacci_rs
rust_fact: src/rust/factorial.rs
	-rustc src/rust/factorial.rs -o bin/fact/factorial_rs
rust_power: src/rust/power.rs
	-rustc src/rust/power.rs -o bin/power/power_rs

# --- Java ---
java_fibo: src/java/Fibonacci.java
	-javac -d bin/fibo src/java/Fibonacci.java
java_fact: src/java/Factorial.java
	-javac -d bin/fact src/java/Factorial.java
java_power: src/java/Power.java
	-javac -d bin/power src/java/Power.java

# --- Fortran ---
fortran_fibo: src/fortran/fibonacci.f90
	-gfortran src/fortran/fibonacci.f90 -o bin/fibo/fibonacci_f90
fortran_fact: src/fortran/factorial.f90
	-gfortran src/fortran/factorial.f90 -o bin/fact/factorial_f90
fortran_power: src/fortran/power.f90
	-gfortran src/fortran/power.f90 -o bin/power/power_f90

# --- FLOAT COMPILE RULES ---
float_compile: float_cpp float_go float_rust float_java float_fortran

# C++ Float
float_cpp:
	-g++ src/cpp/fibonacci_float.cpp -o bin/float/fibo/fibonacci_cpp
	-g++ src/cpp/factorial_float.cpp -o bin/float/fact/factorial_cpp
	-g++ src/cpp/power_float.cpp -o bin/float/power/power_cpp

# Go Float
float_go:
	-go build -o bin/float/fibo/fibonacci_go src/go/fibonacci_float.go
	-go build -o bin/float/fact/factorial_go src/go/factorial_float.go
	-go build -o bin/float/power/power_go src/go/power_float.go

# Rust Float
float_rust:
	-rustc src/rust/fibonacci_float.rs -o bin/float/fibo/fibonacci_rs
	-rustc src/rust/factorial_float.rs -o bin/float/fact/factorial_rs
	-rustc src/rust/power_float.rs -o bin/float/power/power_rs

# Java Float
float_java:
	-javac -d bin/float/fibo src/java/FibonacciFloat.java
	-javac -d bin/float/fact src/java/FactorialFloat.java
	-javac -d bin/float/power src/java/PowerFloat.java

# Fortran Float
float_fortran:
	-gfortran src/fortran/fibonacci_float.f90 -o bin/float/fibo/fibonacci_f90
	-gfortran src/fortran/factorial_float.f90 -o bin/float/fact/factorial_f90
	-gfortran src/fortran/power_float.f90 -o bin/float/power/power_f90

# Phony targets
.PHONY: python js float float_compile

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

# Verify All
verify_all: verify_fibo verify_fact verify_power

verify_fibo: fibo
	@python3 tests/verify_fibonacci.py $(COUNT)

verify_fact: fact
	@python3 tests/verify_factorial.py $(COUNT)

verify_power: power
	@python3 tests/verify_power.py $(BASE) $(EXP)

# Clean up compiled files
clean:
	rm -rf bin
