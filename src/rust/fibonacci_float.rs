use std::env;
use std::time::Instant;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("1475".to_string());
    let count = count_str.parse::<u32>().unwrap_or(1475);

    let mut a = 0.0f64;
    let mut b = 1.0f64;

    let start = Instant::now();
    for _ in 0..count {
        let temp = a;
        a = b;
        b = temp + b;
    }
    let duration = start.elapsed();
    
    println!("Result(F_{}): {:e}", count, a);
    println!("Time: {:.3} ms", duration.as_nanos() as f64 / 1_000_000.0);
}
