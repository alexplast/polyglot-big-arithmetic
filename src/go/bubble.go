package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	N := 10000
	if nStr := os.Getenv("SORT_SIZE"); nStr != "" {
		if val, err := strconv.Atoi(nStr); err == nil {
			N = val
		}
	}

	arr := make([]float64, N)
	var seed uint32 = 42
	
	for i := 0; i < N; i++ {
		seed = seed*1664525 + 1013904223
		arr[i] = float64(seed) / 4294967296.0
	}

	start := time.Now()
	for i := 0; i < N-1; i++ {
		for j := 0; j < N-i-1; j++ {
			if arr[j] > arr[j+1] {
				arr[j], arr[j+1] = arr[j+1], arr[j]
			}
		}
	}
	elapsed := time.Since(start)

	fmt.Printf("Sort(%d): ", N)
	for i := 0; i < 5; i++ { fmt.Printf("%.4f ", arr[i]) }
	fmt.Print("... ")
	for i := N-5; i < N; i++ { fmt.Printf("%.4f ", arr[i]) }
	fmt.Println()
	
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Microseconds())/1000.0)
}
