use std::env;
use std::time::Instant;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("170".to_string());
    let count = count_str.parse::<u64>().unwrap_or(170);

    let mut factorial = 1.0f64;
    
    let start = Instant::now();
    for i in 1..=count {
        factorial *= i as f64;
    }
    let duration = start.elapsed();

    println!("Result({}!): {:e}", count, factorial);
    println!("Time: {:.3} ms", duration.as_nanos() as f64 / 1_000_000.0);
}
