use std::env;
use std::time::Instant;

fn main() {
    let n_str = env::var("SORT_SIZE").unwrap_or("10000".to_string());
    let n = n_str.parse::<usize>().unwrap_or(10000);

    let mut arr = vec![0.0f64; n];
    let mut seed: u32 = 42;
    
    for i in 0..n {
        seed = seed.wrapping_mul(1664525).wrapping_add(1013904223);
        arr[i] = (seed as f64) / 4294967296.0;
    }

    let start = Instant::now();
    for i in 0..n-1 {
        for j in 0..n-i-1 {
            if arr[j] > arr[j+1] {
                arr.swap(j, j+1);
            }
        }
    }
    let duration = start.elapsed();

    print!("Sort({}): ", n);
    for i in 0..5 { print!("{:.4} ", arr[i]); }
    print!("... ");
    for i in n-5..n { print!("{:.4} ", arr[i]); }
    println!();
    
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
