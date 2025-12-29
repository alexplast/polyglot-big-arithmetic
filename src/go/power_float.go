package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"time"
)

func main() {
	base := 2.0
	exp := 1023

	if baseStr := os.Getenv("BASE"); baseStr != "" {
		if val, err := strconv.ParseFloat(baseStr, 64); err == nil {
			base = val
		}
	}

	if expStr := os.Getenv("EXP"); expStr != "" {
		if val, err := strconv.Atoi(expStr); err == nil {
			exp = val
		}
	}

	start := time.Now()
	// Using standard library math.Pow for fairness in "native" float comparison
	result := math.Pow(base, float64(exp))
	elapsed := time.Since(start)

	fmt.Printf("Result(%.2f^%d): %.10e\n", base, exp, result)
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Nanoseconds())/1000000.0)
}
