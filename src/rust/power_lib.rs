use num_bigint::BigInt;
use std::env;
use std::time::Instant;

fn main() {
    let base_str = env::var("BASE").unwrap_or("2".to_string());
    let exp_str = env::var("EXP").unwrap_or("1000".to_string());

    let base_val = base_str.parse::<u64>().unwrap_or(2);
    let exp_val = exp_str.parse::<u32>().unwrap_or(1000);

    let a: BigInt = base_val.into();

    let start = Instant::now();
    // num-bigint pow requires u32
    let result = a.pow(exp_val);
    let duration = start.elapsed();

    println!("Result({}^{}): {}", base_val, exp_val, result);
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
