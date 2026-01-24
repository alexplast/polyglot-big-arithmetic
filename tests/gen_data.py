#!/usr/bin/env python3
import argparse
import struct
import random
import os

DEFAULT_SIZE = 10000
OUTPUT_FILE = "data.bin"

def generate_data(size, filename):
    print(f"Generating {size} random doubles...")
    
    # Fixed seed for absolute reproducibility across runs
    random.seed(42)
    
    with open(filename, "wb") as f:
        for _ in range(size):
            # Generate random float between 0.0 and 1.0
            val = random.random()
            # Pack as little-endian double (8 bytes)
            f.write(struct.pack('<d', val))
            
    print(f"[SUCCESS] Wrote {size * 8} bytes to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate binary data for sort benchmark")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE, help="Number of doubles to generate")
    parser.add_argument("--out", type=str, default=OUTPUT_FILE, help="Output filename")
    
    args = parser.parse_args()
    generate_data(args.size, args.out)

if __name__ == "__main__":
    main()
