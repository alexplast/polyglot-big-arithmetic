use std::env;
use std::time::Instant;
use std::fs::File;
use std::io::Read;

fn main() -> std::io::Result<()> {
    let n_str = env::var("SORT_SIZE").unwrap_or("10000".to_string());
    let n = n_str.parse::<usize>().unwrap_or(10000);

    let mut arr = vec![0.0f64; n];

    // Read data.bin
    let mut file = File::open("data.bin").expect("Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first.");
    
    let mut buffer = vec![0u8; n * 8];
    file.read_exact(&mut buffer).expect("File too short for SORT_SIZE");

    for i in 0..n {
        let mut bytes = [0u8; 8];
        bytes.copy_from_slice(&buffer[i*8 .. (i+1)*8]);
        arr[i] = f64::from_le_bytes(bytes);
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
    let limit = if n < 5 { n } else { 5 };
    for i in 0..limit { print!("{:.4} ", arr[i]); }
    print!("... ");
    if n > 5 {
        for i in n-5..n { print!("{:.4} ", arr[i]); }
    }
    println!();
    
    println!("Time: {:.3} ms", duration.as_micros() as f64 / 1000.0);
    Ok(())
}
