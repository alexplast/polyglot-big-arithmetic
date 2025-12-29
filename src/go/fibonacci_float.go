package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	n := 1475
	countStr := os.Getenv("COUNT")
	if countStr != "" {
		if val, err := strconv.Atoi(countStr); err == nil {
			n = val
		}
	}

	a := 0.0
	b := 1.0
	
	start := time.Now()
	for i := 0; i < n; i++ {
		temp := a
		a = b
		b = temp + b
	}
	elapsed := time.Since(start)

	fmt.Printf("Result(F_%d): %.10e\n", n, a)
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Nanoseconds())/1000000.0)
}
