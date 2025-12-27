use std::env;
use std::time::Instant;

// Multiply two BigInts represented as digit vectors
fn bigint_multiply(a: &[u32], b: &[u32]) -> Vec<u32> {
    let mut result = vec![0u64; a.len() + b.len()];
    
    for i in 0..a.len() {
        let mut carry = 0u64;
        for j in 0..b.len() {
            let current = result[i + j] + (a[i] as u64) * (b[j] as u64) + carry;
            result[i + j] = current % 10;
            carry = current / 10;
        }
        let mut k = b.len();
        while carry > 0 {
            let current = result[i + k] + carry;
            result[i + k] = current % 10;
            carry = current / 10;
            k += 1;
        }
    }
    
    // Remove leading zeros and convert to u32
    while result.len() > 1 && result.last() == Some(&0) {
        result.pop();
    }
    
    result.into_iter().map(|x| x as u32).collect()
}

// Binary exponentiation
fn power(base: u32, exp: u32) -> Vec<u32> {
    let mut result = vec![1u32];
    let mut b = vec![base % 10];
    
    // Convert base to digits
    let mut n = base / 10;
    while n > 0 {
        b.push((n % 10) as u32);
        n /= 10;
    }
    
    let mut e = exp;
    
    while e > 0 {
        if e % 2 == 1 {
            result = bigint_multiply(&result, &b);
        }
        b = bigint_multiply(&b, &b);
        e /= 2;
    }
    
    result
}

fn main() {
    let base: u32 = env::var("BASE")
        .unwrap_or("2".to_string())
        .parse()
        .unwrap_or(2);
    
    let exp: u32 = env::var("EXP")
        .unwrap_or("1000".to_string())
        .parse()
        .unwrap_or(1000);

    let start = Instant::now();
    let result = power(base, exp);
    let duration = start.elapsed();

    print!("Result({}^{}): ", base, exp);
    for &d in result.iter().rev() {
        print!("{}", d);
    }
    println!();
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
