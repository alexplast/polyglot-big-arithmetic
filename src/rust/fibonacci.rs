use std::env;
use std::time::Instant;

struct BigInt {
    digits: Vec<u32>,
}

impl BigInt {
    fn new(mut n: u64) -> Self {
        let mut digits = Vec::new();
        if n == 0 {
            digits.push(0);
        }
        while n > 0 {
            digits.push((n % 10) as u32);
            n /= 10;
        }
        BigInt { digits }
    }

    fn add(&mut self, other: &BigInt) {
        let mut carry = 0u32;
        let n = self.digits.len().max(other.digits.len());
        for i in 0..n {
            if i == self.digits.len() {
                self.digits.push(0);
            }
            let d2 = if i < other.digits.len() { other.digits[i] } else { 0 };
            let sum = self.digits[i] + d2 + carry;
            self.digits[i] = sum % 10;
            carry = sum / 10;
        }
        if carry > 0 {
            self.digits.push(carry);
        }
    }

    fn to_string(&self) -> String {
        self.digits.iter().rev().map(|d| d.to_string()).collect()
    }
}

fn main() {
    let count_str = env::var("COUNT").unwrap_or("10".to_string());
    let count = count_str.parse::<u32>().unwrap_or(10);

    if count == 0 {
        println!("Result(F_0): 0");
        return;
    }

    let mut a = BigInt::new(0);
    let mut b = BigInt::new(1);

    let start = Instant::now();
    for _ in 0..count {
        let temp = BigInt { digits: a.digits.clone() };
        a = BigInt { digits: b.digits.clone() };
        b.add(&temp);
    }
    let duration = start.elapsed();
    println!("Result(F_{}): {}", count, a.to_string());
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
