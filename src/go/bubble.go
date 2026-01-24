package main

import (
	"encoding/binary"
	"fmt"
	"math"
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
	
	f, err := os.Open("data.bin")
	if err != nil {
		fmt.Println("Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first.")
		os.Exit(1)
	}
	defer f.Close()

	// Reading bytes and converting manually is often faster/safer for large arrays 
	// than binary.Read with reflection, but for 10k items binary.Read is fine.
	// However, let's do it optimally: read all bytes, then convert.
	bytes := make([]byte, N*8)
	_, err = f.Read(bytes)
	if err != nil {
		fmt.Println("Error reading file:", err)
		os.Exit(1)
	}

	for i := 0; i < N; i++ {
		bits := binary.LittleEndian.Uint64(bytes[i*8 : (i+1)*8])
		arr[i] = math.Float64frombits(bits)
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
	limit := 5
	if N < 5 { limit = N }
	for i := 0; i < limit; i++ { fmt.Printf("%.4f ", arr[i]) }
	fmt.Print("... ")
	if N > 5 {
		for i := N-5; i < N; i++ { fmt.Printf("%.4f ", arr[i]) }
	}
	fmt.Println()
	
	fmt.Printf("Time: %.3f ms\n", float64(elapsed.Microseconds())/1000.0)
}
