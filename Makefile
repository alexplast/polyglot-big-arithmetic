# Makefile for Polyglot Math Benchmark

CXX = g++ -std=c++11
CC = gcc
PYTHON = python3
DOCKER_IMG = polyglot-bench
DATA_SIZE ?= 10000
DATA_SEED ?= 1337
RUNNER_ARGS ?=
UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)
ASM_SUPPORTED := 0

ifeq ($(UNAME_S),Linux)
ifeq ($(UNAME_M),x86_64)
ASM_SUPPORTED := 1
endif
endif

all: fibo fact power matrix float sort

# --- Compile Groups ---
fibo: bin_dirs cpp_fibo cpp_gmp_fibo c_fibo go_fibo rust_fibo rust_lib_fibo java_fibo fortran_fibo
fact: bin_dirs cpp_fact cpp_gmp_fact c_fact go_fact rust_fact rust_lib_fact java_fact fortran_fact
power: bin_dirs cpp_power cpp_gmp_power c_power go_power rust_power rust_lib_power java_power fortran_power
matrix: bin_dirs cpp_matrix c_matrix asm_matrix go_matrix rust_matrix java_matrix fortran_matrix
float: bin_dirs float_compile
sort: bin_dirs sort_compile

bin_dirs:
	@mkdir -p bin/fibo bin/fact bin/power bin/matrix bin/sort
	@mkdir -p bin/float/fibo bin/float/fact bin/float/power
	@mkdir -p results

# --- Sort Compiles ---
sort_compile: cpp_sort c_sort go_sort rust_sort java_sort fortran_sort asm_sort

cpp_sort: src/cpp/bubble.cpp
	$(CXX) -O3 src/cpp/bubble.cpp -o bin/sort/bubble_cpp

c_sort: src/c/bubble.c
	$(CC) -O3 src/c/bubble.c -o bin/sort/bubble_c

go_sort: src/go/bubble.go
	go build -o bin/sort/bubble_go src/go/bubble.go

rust_sort: src/rust/bubble.rs
	rustc -C opt-level=3 src/rust/bubble.rs -o bin/sort/bubble_rs

java_sort: src/java/Bubble.java
	javac -d bin/sort src/java/Bubble.java

fortran_sort: src/fortran/bubble.f90
	gfortran -O3 src/fortran/bubble.f90 -o bin/sort/bubble_f90

# --- CPP Naive & GMP ---
cpp_fibo: src/cpp/fibonacci.cpp
	$(CXX) -O3 src/cpp/fibonacci.cpp -o bin/fibo/fibonacci_cpp
cpp_fact: src/cpp/factorial.cpp
	$(CXX) -O3 src/cpp/factorial.cpp -o bin/fact/factorial_cpp
cpp_power: src/cpp/power.cpp
	$(CXX) -O3 src/cpp/power.cpp -o bin/power/power_cpp
cpp_matrix: src/cpp/matrix.cpp
	$(CXX) -O3 src/cpp/matrix.cpp -o bin/matrix/matrix_cpp

# GMP requires libgmp-dev installed and -lgmpxx -lgmp flags
cpp_gmp_fibo: src/cpp/fibonacci_gmp.cpp
	$(CXX) -O3 src/cpp/fibonacci_gmp.cpp -o bin/fibo/fibonacci_cpp_gmp -lgmpxx -lgmp
cpp_gmp_fact: src/cpp/factorial_gmp.cpp
	$(CXX) -O3 src/cpp/factorial_gmp.cpp -o bin/fact/factorial_cpp_gmp -lgmpxx -lgmp
cpp_gmp_power: src/cpp/power_gmp.cpp
	$(CXX) -O3 src/cpp/power_gmp.cpp -o bin/power/power_cpp_gmp -lgmpxx -lgmp

# --- C Compiles ---
c_fibo: src/c/fibonacci.c
	$(CC) -O3 src/c/fibonacci.c -o bin/fibo/fibonacci_c
c_fact: src/c/factorial.c
	$(CC) -O3 src/c/factorial.c -o bin/fact/factorial_c
c_power: src/c/power.c
	$(CC) -O3 src/c/power.c -o bin/power/power_c
c_matrix: src/c/matrix.c
	$(CC) -O3 src/c/matrix.c -o bin/matrix/matrix_c

asm_matrix: src/asm/matrix.s
ifeq ($(ASM_SUPPORTED),1)
	gcc -no-pie src/asm/matrix.s -o bin/matrix/matrix_asm
else
	@echo "Skipping asm matrix build: GNU/Linux x86_64 only"
	@rm -f bin/matrix/matrix_asm
endif

asm_sort: src/asm/bubble.s
ifeq ($(ASM_SUPPORTED),1)
	gcc -no-pie src/asm/bubble.s -o bin/sort/bubble_asm
else
	@echo "Skipping asm sort build: GNU/Linux x86_64 only"
	@rm -f bin/sort/bubble_asm
endif

go_fibo: src/go/fibonacci.go
	go build -o bin/fibo/fibonacci_go src/go/fibonacci.go
go_fact: src/go/factorial.go
	go build -o bin/fact/factorial_go src/go/factorial.go
go_power: src/go/power.go
	go build -o bin/power/power_go src/go/power.go
go_matrix: src/go/matrix.go
	go build -o bin/matrix/matrix_go src/go/matrix.go

# --- Rust Native ---
rust_fibo: src/rust/fibonacci.rs
	rustc -C opt-level=3 src/rust/fibonacci.rs -o bin/fibo/fibonacci_rs
rust_fact: src/rust/factorial.rs
	rustc -C opt-level=3 src/rust/factorial.rs -o bin/fact/factorial_rs
rust_power: src/rust/power.rs
	rustc -C opt-level=3 src/rust/power.rs -o bin/power/power_rs
rust_matrix: src/rust/matrix.rs
	rustc -C opt-level=3 src/rust/matrix.rs -o bin/matrix/matrix_rs

# --- Rust Lib (Cargo) ---
rust_lib_build: src/rust/Cargo.toml
	@echo "Building Rust Libs with Cargo..."
	cd src/rust && cargo build --release --quiet --bins

rust_lib_fibo: rust_lib_build
	cp src/rust/target/release/fibonacci_lib bin/fibo/fibonacci_rs_lib

rust_lib_fact: rust_lib_build
	cp src/rust/target/release/factorial_lib bin/fact/factorial_rs_lib

rust_lib_power: rust_lib_build
	cp src/rust/target/release/power_lib bin/power/power_rs_lib

java_fibo: src/java/Fibonacci.java
	javac -d bin/fibo src/java/Fibonacci.java
java_fact: src/java/Factorial.java
	javac -d bin/fact src/java/Factorial.java
java_power: src/java/Power.java
	javac -d bin/power src/java/Power.java
java_matrix: src/java/Matrix.java
	javac -d bin/matrix src/java/Matrix.java

fortran_fibo: src/fortran/fibonacci.f90
	gfortran -O3 src/fortran/fibonacci.f90 -o bin/fibo/fibonacci_f90
fortran_fact: src/fortran/factorial.f90
	gfortran -O3 src/fortran/factorial.f90 -o bin/fact/factorial_f90
fortran_power: src/fortran/power.f90
	gfortran -O3 src/fortran/power.f90 -o bin/power/power_f90
fortran_matrix: src/fortran/matrix.f90
	gfortran -O3 src/fortran/matrix.f90 -o bin/matrix/matrix_f90

float_compile:
	$(CXX) -O3 src/cpp/fibonacci_float.cpp -o bin/float/fibo/fibonacci_cpp
	$(CXX) -O3 src/cpp/factorial_float.cpp -o bin/float/fact/factorial_cpp
	$(CXX) -O3 src/cpp/power_float.cpp -o bin/float/power/power_cpp
	$(CC) -O3 src/c/fibonacci_float.c -o bin/float/fibo/fibonacci_c
	$(CC) -O3 src/c/factorial_float.c -o bin/float/fact/factorial_c
	$(CC) -O3 src/c/power_float.c -o bin/float/power/power_c
	go build -o bin/float/fibo/fibonacci_go src/go/fibonacci_float.go
	go build -o bin/float/fact/factorial_go src/go/factorial_float.go
	go build -o bin/float/power/power_go src/go/power_float.go
	rustc -C opt-level=3 src/rust/fibonacci_float.rs -o bin/float/fibo/fibonacci_rs
	rustc -C opt-level=3 src/rust/factorial_float.rs -o bin/float/fact/factorial_rs
	rustc -C opt-level=3 src/rust/power_float.rs -o bin/float/power/power_rs
	javac -d bin/float/fibo src/java/FibonacciFloat.java
	javac -d bin/float/fact src/java/FactorialFloat.java
	javac -d bin/float/power src/java/PowerFloat.java
	gfortran -O3 src/fortran/fibonacci_float.f90 -o bin/float/fibo/fibonacci_f90
	gfortran -O3 src/fortran/factorial_float.f90 -o bin/float/fact/factorial_f90
	gfortran -O3 src/fortran/power_float.f90 -o bin/float/power/power_f90

# --- Runners ---

data:
	@$(PYTHON) tests/gen_data.py --size $(DATA_SIZE) --seed $(DATA_SEED)

test: all data
	@echo "--- Verifying Implementations ---"
	@$(PYTHON) tests/verify_factorial.py
	@$(PYTHON) tests/verify_fibonacci.py
	@$(PYTHON) tests/verify_power.py
	@$(PYTHON) tests/verify_matrix.py
	@DATA_SEED=$(DATA_SEED) $(PYTHON) tests/verify_sort.py

bench_all: all data
	@DATA_SEED=$(DATA_SEED) $(PYTHON) tests/runner.py --bench all $(RUNNER_ARGS)

bench_smoke: all data
	@DATA_SEED=$(DATA_SEED) $(PYTHON) tests/runner.py --bench all --profile smoke --runs 1 --warmup 0 --no-plots --no-report --results-dir results/smoke --meta results/smoke/meta.json

clean:
	rm -rf bin results data.bin
	rm -rf src/rust/target src/rust/Cargo.lock

# --- Docker ---

docker_build:
	docker build -t $(DOCKER_IMG) .

docker_run:
	@echo "Running benchmark inside Docker container..."
	@# We mount a named volume 'polyglot_cargo_cache' to persist crate downloads
	docker run --rm \
		-v "$(PWD)":/app \
		-v polyglot_cargo_cache:/usr/local/cargo \
		-w /app \
		$(DOCKER_IMG) make bench_all DATA_SIZE="$(DATA_SIZE)" DATA_SEED="$(DATA_SEED)" RUNNER_ARGS="$(RUNNER_ARGS)"

docker_smoke:
	@echo "Running smoke benchmark inside Docker container..."
	docker run --rm \
		-v "$(PWD)":/app \
		-v polyglot_cargo_cache:/usr/local/cargo \
		-w /app \
		$(DOCKER_IMG) make bench_smoke DATA_SIZE="$(DATA_SIZE)" DATA_SEED="$(DATA_SEED)"

docker_test:
	@echo "Running verification inside Docker container..."
	docker run --rm \
		-v "$(PWD)":/app \
		-v polyglot_cargo_cache:/usr/local/cargo \
		-w /app \
		$(DOCKER_IMG) make test DATA_SIZE="$(DATA_SIZE)" DATA_SEED="$(DATA_SEED)"

docker_shell:
	@echo "Starting shell inside Docker..."
	docker run --rm -it \
		-v "$(PWD)":/app \
		-v polyglot_cargo_cache:/usr/local/cargo \
		-w /app \
		$(DOCKER_IMG) /bin/bash

help:
	@echo "Available commands:"
	@echo "  make bench_all    - Run benchmarks locally"
	@echo "  make bench_smoke  - Run a fast local smoke benchmark"
	@echo "  make test         - Run correctness verification locally"
	@echo "  make docker_build - Build the Docker environment"
	@echo "  make docker_run   - Run benchmarks inside Docker"
	@echo "  make docker_smoke - Run a fast smoke benchmark inside Docker"
	@echo "  make docker_test  - Run verification inside Docker"
	@echo "  make docker_shell - Open a shell inside Docker"
	@echo "  make clean        - Remove artifacts"
