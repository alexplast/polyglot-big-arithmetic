package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
)

func main() {
	n := 10 // Default value
	countStr := os.Getenv("COUNT")
	if countStr != "" {
		parsedCount, err := strconv.Atoi(countStr)
		if err == nil {
			n = parsedCount
		} else {
			fmt.Printf("Error converting COUNT environment variable: %v\n", err)
		}
	}

	fmt.Printf("Fibonacci Sequence (first %d numbers):\n", n)

	a := big.NewInt(0)
	b := big.NewInt(1)
	for i := 0; i < n; i++ {
		fmt.Printf("%d ", a)
		temp := new(big.Int)
		temp.Set(a)
		a.Set(b)
		b.Add(temp, b)
	}
	fmt.Println()
}
