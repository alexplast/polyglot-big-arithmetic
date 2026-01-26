use num_bigint::BigInt;
use num_traits::{Zero, One};
use std::env;
use std::time::Instant;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("10".to_string());
    let count = count_str.parse::<usize>().unwrap_or(10);

    let mut a: BigInt = Zero::zero();
    let mut b: BigInt = One::one();

    let start = Instant::now();
    for _ in 0..count {
        let temp = a.clone();
        a = b.clone();
        b = b + temp;
    }
    let duration = start.elapsed();

    println!("Result(F_{}): {}", count, a);
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
