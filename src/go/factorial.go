package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
)

func main() {
	count := 200 // Default to high number for arbitrary precision 
	countStr := os.Getenv("COUNT")
	if countStr != "" {
		if val, err := strconv.Atoi(countStr); err == nil {
			count = val
		}
	}

	// fmt.Printf("Calculating Factorial(%d)...\n", count)
	
	fact := big.NewInt(1)

	for i := 1; i <= count; i++ {
		bigI := big.NewInt(int64(i))
		fact.Mul(fact, bigI)
	}
	fmt.Printf("Result(%d!): %s\n", count, fact.String())
}
