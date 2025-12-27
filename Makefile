# Makefile for compiling Fibonacci applications

COUNT ?= 10

# Default target: build all applications
all: bin_dir cpp go rust java fortran

bin_dir:
	@mkdir -p bin

# C++
cpp: src/cpp/fibonacci.cpp
	-g++ src/cpp/fibonacci.cpp -o bin/fibonacci_cpp

# Go
go: src/go/fibonacci.go
	-go build -o bin/fibonacci_go src/go/fibonacci.go

# Rust
rust: src/rust/fibonacci.rs
	-rustc src/rust/fibonacci.rs -o bin/fibonacci_rs

# Java
java: src/java/Fibonacci.java
	-javac -d bin src/java/Fibonacci.java

# Fortran
fortran: src/fortran/fibonacci.f90
	-gfortran src/fortran/fibonacci.f90 -o bin/fibonacci_f90

# Phony targets for interpreted languages
.PHONY: python js
python:
	@echo "Python is an interpreted language, no compilation needed."

js:
	@echo "JavaScript (Node.js) is interpreted, no compilation needed."

# Run all applications
run: all
	@echo "Running C++ Fibonacci:"
	-@time env COUNT=$(COUNT) ./bin/fibonacci_cpp
	@echo "\nRunning Go Fibonacci:"
	-@time env COUNT=$(COUNT) ./bin/fibonacci_go
	@echo "\nRunning Rust Fibonacci:"
	-@time env COUNT=$(COUNT) ./bin/fibonacci_rs
	@echo "\nRunning Java Fibonacci:"
	-@time env COUNT=$(COUNT) java -cp bin Fibonacci
	@echo "\nRunning Fortran Fibonacci:"
	-@time env COUNT=$(COUNT) ./bin/fibonacci_f90
	@echo "\nRunning Python Fibonacci:"
	-@time env COUNT=$(COUNT) python3 src/python/fibonacci.py
	@echo "\nRunning JavaScript Fibonacci:"
	-@time env COUNT=$(COUNT) node src/js/fibonacci.js

# Clean up compiled files
clean:
	rm -rf bin

