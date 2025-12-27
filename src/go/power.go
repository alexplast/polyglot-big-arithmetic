package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
	"time"
)

func main() {
	base := 2
	exp := 1000

	if baseStr := os.Getenv("BASE"); baseStr != "" {
		if val, err := strconv.Atoi(baseStr); err == nil {
			base = val
		}
	}

	if expStr := os.Getenv("EXP"); expStr != "" {
		if val, err := strconv.Atoi(expStr); err == nil {
			exp = val
		}
	}

	bigBase := big.NewInt(int64(base))
	bigExp := big.NewInt(int64(exp))
	result := new(big.Int)

	start := time.Now()
	result.Exp(bigBase, bigExp, nil)
	elapsed := time.Since(start)

	fmt.Printf("Result(%d^%d): %s\n", base, exp, result.String())
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Microseconds())/1000.0)
}
