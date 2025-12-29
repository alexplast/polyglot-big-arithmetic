use std::env;
use std::time::Instant;

fn main() {
    let n_str = env::var("MATRIX_SIZE").unwrap_or("256".to_string());
    let n = n_str.parse::<usize>().unwrap_or(256);

    let mut a = vec![0.0f64; n * n];
    let mut b = vec![0.0f64; n * n];
    let mut c = vec![0.0f64; n * n];

    for i in 0..(n*n) {
        a[i] = 1.0 + (i % 100) as f64 * 0.01;
        b[i] = 1.0 - (i % 100) as f64 * 0.01;
    }

    let start = Instant::now();

    // Matrix Multiplication
    for i in 0..n {
        for k in 0..n {
            let r = a[i * n + k];
            for j in 0..n {
                c[i * n + j] += r * b[k * n + j];
            }
        }
    }

    let duration = start.elapsed();

    println!("Matrix({}x{})", n, n);
    println!("Result[0]: {}", c[0]);
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
}
