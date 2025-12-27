use std::env;
use std::time::Instant;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("200".to_string());
    let count = count_str.parse::<u32>().unwrap_or(200);

    let mut digits = vec![1u32];
    
    let start = Instant::now();
    for i in 2..=count {
        let mut carry = 0u64;
        for j in 0..digits.len() {
            let current = digits[j] as u64 * i as u64 + carry;
            digits[j] = (current % 10) as u32;
            carry = current / 10;
        }
        while carry > 0 {
            digits.push((carry % 10) as u32);
            carry /= 10;
        }
    }
    let duration = start.elapsed();

    print!("Result({}!): ", count);
    for &d in digits.iter().rev() {
        print!("{}", d);
    }
    println!();
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
