package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func main() {
	count := 170
	countStr := os.Getenv("COUNT")
	if countStr != "" {
		if val, err := strconv.Atoi(countStr); err == nil {
			count = val
		}
	}

	factorial := 1.0
	start := time.Now()
	for i := 1; i <= count; i++ {
		factorial *= float64(i)
	}
	elapsed := time.Since(start)
	
	fmt.Printf("Result(%d!): %.10e\n", count, factorial)
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Nanoseconds())/1000000.0)
}
