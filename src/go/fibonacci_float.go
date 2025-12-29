package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	n := 1475
	if countStr := os.Getenv("COUNT"); countStr != "" {
		if val, err := strconv.Atoi(countStr); err == nil {
			n = val
		}
	}

	var a, b float64
	
	start := time.Now()
	for k := 0; k < 200000; k++ {
		a = 0.0
		b = 1.0
		for i := 0; i < n; i++ {
			temp := a
			a = b
			b = temp + b
		}
	}
	elapsed := time.Since(start)

	fmt.Printf("Result: %e\n", a)
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Milliseconds()))
}
