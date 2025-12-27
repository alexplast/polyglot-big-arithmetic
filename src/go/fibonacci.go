package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
	"time"
)

func main() {
	n := 10
	countStr := os.Getenv("COUNT")
	if countStr != "" {
		if val, err := strconv.Atoi(countStr); err == nil {
			n = val
		}
	}

	a := big.NewInt(0)
	b := big.NewInt(1)
	start := time.Now()
	for i := 0; i < n; i++ {
		temp := new(big.Int).Set(a)
		a.Set(b)
		b.Add(temp, b)
	}
	elapsed := time.Since(start)
	fmt.Printf("Result(F_%d): %d\n", n, a)
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Microseconds())/1000.0)
}
