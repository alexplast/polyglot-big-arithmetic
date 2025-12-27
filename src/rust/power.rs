use std::env;
use std::time::Instant;

const BASE: u64 = 1_000_000_000;

// Multiply two BigInts represented as digit vectors (Base 10^9)
fn bigint_multiply(a: &[u64], b: &[u64]) -> Vec<u64> {
    if a.is_empty() || b.is_empty() {
        return vec![0];
    }
    
    let mut result = vec![0u64; a.len() + b.len()];
    
    for i in 0..a.len() {
        let mut carry = 0u64;
        for j in 0..b.len() {
            let current = result[i + j] + (a[i] * b[j]) + carry;
            result[i + j] = current % BASE;
            carry = current / BASE;
        }
        let mut k = b.len();
        while carry > 0 {
            let current = result[i + k] + carry;
            result[i + k] = current % BASE;
            carry = current / BASE;
            k += 1;
        }
    }
    
    // Remove leading zeros
    while result.len() > 1 && result.last() == Some(&0) {
        result.pop();
    }
    
    result
}

// Binary exponentiation
fn power(base: u64, exp: u64) -> Vec<u64> {
    let mut result = vec![1u64];
    
    // Convert base to digits (Base 10^9)
    let mut b_vec = Vec::new();
    let mut temp_base = base;
    if temp_base == 0 {
        b_vec.push(0);
    }
    while temp_base > 0 {
        b_vec.push(temp_base % BASE);
        temp_base /= BASE;
    }
    
    let mut e = exp;
    
    while e > 0 {
        if e % 2 == 1 {
            result = bigint_multiply(&result, &b_vec);
        }
        b_vec = bigint_multiply(&b_vec, &b_vec);
        e /= 2;
    }
    
    result
}

fn main() {
    let base: u64 = env::var("BASE")
        .unwrap_or("2".to_string())
        .parse()
        .unwrap_or(2);
    
    let exp: u64 = env::var("EXP")
        .unwrap_or("1000".to_string())
        .parse()
        .unwrap_or(1000);

    let start = Instant::now();
    let result = power(base, exp);
    let duration = start.elapsed();

    print!("Result({}^{}): ", base, exp);
    if result.is_empty() {
        print!("0");
    } else {
        print!("{}", result.last().unwrap());
        for d in result.iter().rev().skip(1) {
            print!("{:09}", d);
        }
    }
    println!();
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
