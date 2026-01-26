use num_bigint::BigInt;
use std::env;
use std::time::Instant;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("200".to_string());
    let count = count_str.parse::<u64>().unwrap_or(200);

    let mut fact: BigInt = 1.into();

    let start = Instant::now();
    for i in 1..=count {
        fact = fact * i;
    }
    let duration = start.elapsed();

    println!("Result({}!): {}", count, fact);
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
