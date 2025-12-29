package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	N := 256
	if nStr := os.Getenv("MATRIX_SIZE"); nStr != "" {
		if val, err := strconv.Atoi(nStr); err == nil {
			N = val
		}
	}

	A := make([]float64, N*N)
	B := make([]float64, N*N)
	C := make([]float64, N*N)

	for i := 0; i < N*N; i++ {
		A[i] = 1.0 + float64(i%100)*0.01
		B[i] = 1.0 - float64(i%100)*0.01
	}

	start := time.Now()

	for i := 0; i < N; i++ {
		for k := 0; k < N; k++ {
			r := A[i*N+k]
			for j := 0; j < N; j++ {
				C[i*N+j] += r * B[k*N+j]
			}
		}
	}

	elapsed := time.Since(start)

	fmt.Printf("Matrix(%dx%d)\n", N, N)
	fmt.Printf("Result[0]: %.4f\n", C[0])
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Microseconds())/1000.0)
}
