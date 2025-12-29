use std::env;
use std::time::Instant;

fn main() {
    let base: f64 = env::var("BASE")
        .unwrap_or("2".to_string())
        .parse()
        .unwrap_or(2.0);
    
    let exp: i32 = env::var("EXP")
        .unwrap_or("1023".to_string())
        .parse()
        .unwrap_or(1023);

    let start = Instant::now();
    let result = base.powi(exp); // powi is for integer exponent, native f64 method
    let duration = start.elapsed();

    println!("Result({}^{}): {:e}", base, exp, result);
    println!("Time: {:.3} ms", duration.as_nanos() as f64 / 1_000_000.0);
}
