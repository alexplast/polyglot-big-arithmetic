# Makefile for compiling Fibonacci applications

COUNT ?= 10

# Default target: build all applications
all: fibonacci_cpp fibonacci_go fibonacci_rs Fibonacci.class fibonacci_f90

# C++
fibonacci_cpp: fibonacci.cpp
	-g++ fibonacci.cpp -o fibonacci_cpp

# Go
fibonacci_go: fibonacci.go
	-go build -o fibonacci_go fibonacci.go

# Rust
fibonacci_rs: fibonacci.rs
	-rustc fibonacci.rs -o fibonacci_rs

# Java
Fibonacci.class: Fibonacci.java
	-javac Fibonacci.java

# Fortran
fibonacci_f90: fibonacci.f90
	-gfortran fibonacci.f90 -o fibonacci_f90

# Phony targets for interpreted languages (no compilation needed)
.PHONY: python js
python:
	@echo "Python is an interpreted language, no compilation needed."

js:
	@echo "JavaScript (Node.js) is interpreted, no compilation needed."

# Run all applications (ignore errors to run all)
run:
	@echo "Running C++ Fibonacci:"
	-@time env COUNT=$(COUNT) ./fibonacci_cpp
	@echo "\nRunning Go Fibonacci:"
	-@time env COUNT=$(COUNT) ./fibonacci_go
	@echo "\nRunning Rust Fibonacci:"
	-@time env COUNT=$(COUNT) ./fibonacci_rs
	@echo "\nRunning Java Fibonacci:"
	-@time env COUNT=$(COUNT) java Fibonacci
	@echo "\nRunning Fortran Fibonacci:"
	-@time env COUNT=$(COUNT) ./fibonacci_f90
	@echo "\nRunning Python Fibonacci:"
	-@time env COUNT=$(COUNT) python3 fibonacci.py
	@echo "\nRunning JavaScript Fibonacci:"
	-@time env COUNT=$(COUNT) node fibonacci.js

# Clean up compiled files
clean:
	rm -f fibonacci_cpp fibonacci_go fibonacci_rs Fibonacci.class fibonacci_f90

