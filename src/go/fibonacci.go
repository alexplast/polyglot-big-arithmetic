package main

import (
	"fmt"
	"math/big"
	"os"
	"strconv"
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
	for i := 0; i < n; i++ {
		temp := new(big.Int).Set(a)
		a.Set(b)
		b.Add(temp, b)
	}
	fmt.Printf("Result(F_%d): %d\n", n, a)
}
