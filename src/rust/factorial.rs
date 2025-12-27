use std::env;
use std::time::Instant;

const BASE: u64 = 1_000_000_000;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("200".to_string());
    let count = count_str.parse::<u64>().unwrap_or(200);

    // digits stores chunks of 9 digits. 
    // digits[0] is the least significant chunk.
    let mut digits: Vec<u64> = vec![1]; 
    
    let start = Instant::now();
    for i in 2..=count {
        let mut carry = 0u64;
        for j in 0..digits.len() {
            let current = digits[j] * i + carry;
            digits[j] = current % BASE;
            carry = current / BASE;
        }
        while carry > 0 {
            digits.push(carry % BASE);
            carry /= BASE;
        }
    }
    let duration = start.elapsed();

    print!("Result({}!): ", count);
    if digits.is_empty() {
        print!("0");
    } else {
        // Print the most significant chunk normally
        print!("{}", digits.last().unwrap());
        // Print remaining chunks with zero padding
        for d in digits.iter().rev().skip(1) {
            print!("{:09}", d);
        }
    }
    println!();
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
