use std::env;
use std::time::Instant;

const BASE: u64 = 1_000_000_000;

struct BigInt {
    digits: Vec<u64>,
}

impl BigInt {
    fn new(mut n: u64) -> Self {
        let mut digits = Vec::new();
        if n == 0 {
            digits.push(0);
        }
        while n > 0 {
            digits.push(n % BASE);
            n /= BASE;
        }
        BigInt { digits }
    }

    fn add(&mut self, other: &BigInt) {
        let mut carry = 0u64;
        let n = self.digits.len().max(other.digits.len());
        for i in 0..n {
            if i == self.digits.len() {
                self.digits.push(0);
            }
            let d2 = if i < other.digits.len() { other.digits[i] } else { 0 };
            let sum = self.digits[i] + d2 + carry;
            self.digits[i] = sum % BASE;
            carry = sum / BASE;
        }
        if carry > 0 {
            self.digits.push(carry);
        }
    }

    fn print(&self) {
        if self.digits.is_empty() {
            print!("0");
            return;
        }
        print!("{}", self.digits.last().unwrap());
        for d in self.digits.iter().rev().skip(1) {
            print!("{:09}", d);
        }
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
    
    print!("Result(F_{}): ", count);
    a.print();
    println!();
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
