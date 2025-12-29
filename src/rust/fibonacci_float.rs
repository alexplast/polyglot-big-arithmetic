use std::env;
use std::time::Instant;

fn main() {
    let count_str = env::var("COUNT").unwrap_or("1475".to_string());
    let count = count_str.parse::<u32>().unwrap_or(1475);

    let mut a = 0.0f64;
    // Fix: declare b without init, or just assign inside loop. 
    // Compiler warned because we overwrite it immediately in the loop.
    #[allow(unused_assignments)]
    let mut b = 1.0f64;

    let start = Instant::now();
    for _ in 0..200000 {
        a = 0.0; 
        b = 1.0;
        for _ in 0..count {
            let temp = a;
            a = b;
            b = temp + b;
        }
    }
    let duration = start.elapsed();
    
    // Use b to prevent optimization removing it (though a depends on b, so it's fine)
    // Just printing a is enough.
    println!("Result: {:e}", a);
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
