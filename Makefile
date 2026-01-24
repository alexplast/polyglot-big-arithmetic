# Makefile for Polyglot Math Benchmark

CXX = g++ -std=c++11
CC = gcc

all: fibo fact power matrix float sort

# --- Compile Groups ---
fibo: bin_dirs cpp_fibo c_fibo go_fibo rust_fibo java_fibo fortran_fibo
fact: bin_dirs cpp_fact c_fact go_fact rust_fact java_fact fortran_fact
power: bin_dirs cpp_power c_power go_power rust_power java_power fortran_power
matrix: bin_dirs cpp_matrix c_matrix asm_matrix go_matrix rust_matrix java_matrix fortran_matrix
float: bin_dirs float_compile
sort: bin_dirs sort_compile

bin_dirs:
	@mkdir -p bin/fibo bin/fact bin/power bin/matrix bin/sort
	@mkdir -p bin/float/fibo bin/float/fact bin/float/power
	@mkdir -p results

# --- Sort Compiles ---
sort_compile:
	-$(CXX) -O3 src/cpp/bubble.cpp -o bin/sort/bubble_cpp
	-$(CC) -O3 src/c/bubble.c -o bin/sort/bubble_c
	-go build -o bin/sort/bubble_go src/go/bubble.go
	-rustc -C opt-level=3 src/rust/bubble.rs -o bin/sort/bubble_rs
	-javac -d bin/sort src/java/Bubble.java
	-gfortran -O3 src/fortran/bubble.f90 -o bin/sort/bubble_f90
	-gcc -no-pie src/asm/bubble.s -o bin/sort/bubble_asm

# --- Other Compiles ---
cpp_fibo: src/cpp/fibonacci.cpp
	-$(CXX) -O3 src/cpp/fibonacci.cpp -o bin/fibo/fibonacci_cpp
cpp_fact: src/cpp/factorial.cpp
	-$(CXX) -O3 src/cpp/factorial.cpp -o bin/fact/factorial_cpp
cpp_power: src/cpp/power.cpp
	-$(CXX) -O3 src/cpp/power.cpp -o bin/power/power_cpp
cpp_matrix: src/cpp/matrix.cpp
	-$(CXX) -O3 src/cpp/matrix.cpp -o bin/matrix/matrix_cpp

c_fibo: src/c/fibonacci.c
	-$(CC) -O3 src/c/fibonacci.c -o bin/fibo/fibonacci_c
c_fact: src/c/factorial.c
	-$(CC) -O3 src/c/factorial.c -o bin/fact/factorial_c
c_power: src/c/power.c
	-$(CC) -O3 src/c/power.c -o bin/power/power_c
c_matrix: src/c/matrix.c
	-$(CC) -O3 src/c/matrix.c -o bin/matrix/matrix_c

asm_matrix: src/asm/matrix.s
	-gcc -no-pie src/asm/matrix.s -o bin/matrix/matrix_asm

go_fibo: src/go/fibonacci.go
	-go build -o bin/fibo/fibonacci_go src/go/fibonacci.go
go_fact: src/go/factorial.go
	-go build -o bin/fact/factorial_go src/go/factorial.go
go_power: src/go/power.go
	-go build -o bin/power/power_go src/go/power.go
go_matrix: src/go/matrix.go
	-go build -o bin/matrix/matrix_go src/go/matrix.go

rust_fibo: src/rust/fibonacci.rs
	-rustc -C opt-level=3 src/rust/fibonacci.rs -o bin/fibo/fibonacci_rs
rust_fact: src/rust/factorial.rs
	-rustc -C opt-level=3 src/rust/factorial.rs -o bin/fact/factorial_rs
rust_power: src/rust/power.rs
	-rustc -C opt-level=3 src/rust/power.rs -o bin/power/power_rs
rust_matrix: src/rust/matrix.rs
	-rustc -C opt-level=3 src/rust/matrix.rs -o bin/matrix/matrix_rs

java_fibo: src/java/Fibonacci.java
	-javac -d bin/fibo src/java/Fibonacci.java
java_fact: src/java/Factorial.java
	-javac -d bin/fact src/java/Factorial.java
java_power: src/java/Power.java
	-javac -d bin/power src/java/Power.java
java_matrix: src/java/Matrix.java
	-javac -d bin/matrix src/java/Matrix.java

fortran_fibo: src/fortran/fibonacci.f90
	-gfortran -O3 src/fortran/fibonacci.f90 -o bin/fibo/fibonacci_f90
fortran_fact: src/fortran/factorial.f90
	-gfortran -O3 src/fortran/factorial.f90 -o bin/fact/factorial_f90
fortran_power: src/fortran/power.f90
	-gfortran -O3 src/fortran/power.f90 -o bin/power/power_f90
fortran_matrix: src/fortran/matrix.f90
	-gfortran -O3 src/fortran/matrix.f90 -o bin/matrix/matrix_f90

float_compile:
	-$(CXX) -O3 src/cpp/fibonacci_float.cpp -o bin/float/fibo/fibonacci_cpp
	-$(CXX) -O3 src/cpp/factorial_float.cpp -o bin/float/fact/factorial_cpp
	-$(CXX) -O3 src/cpp/power_float.cpp -o bin/float/power/power_cpp
	-$(CC) -O3 src/c/fibonacci_float.c -o bin/float/fibo/fibonacci_c
	-$(CC) -O3 src/c/factorial_float.c -o bin/float/fact/factorial_c
	-$(CC) -O3 src/c/power_float.c -o bin/float/power/power_c
	-go build -o bin/float/fibo/fibonacci_go src/go/fibonacci_float.go
	-go build -o bin/float/fact/factorial_go src/go/factorial_float.go
	-go build -o bin/float/power/power_go src/go/power_float.go
	-rustc -C opt-level=3 src/rust/fibonacci_float.rs -o bin/float/fibo/fibonacci_rs
	-rustc -C opt-level=3 src/rust/factorial_float.rs -o bin/float/fact/factorial_rs
	-rustc -C opt-level=3 src/rust/power_float.rs -o bin/float/power/power_rs
	-javac -d bin/float/fibo src/java/FibonacciFloat.java
	-javac -d bin/float/fact src/java/FactorialFloat.java
	-javac -d bin/float/power src/java/PowerFloat.java
	-gfortran -O3 src/fortran/fibonacci_float.f90 -o bin/float/fibo/fibonacci_f90
	-gfortran -O3 src/fortran/factorial_float.f90 -o bin/float/fact/factorial_f90
	-gfortran -O3 src/fortran/power_float.f90 -o bin/float/power/power_f90

# --- Runners ---
bench_all: all
	@python3 tests/runner.py --bench all

clean:
	rm -rf bin results
