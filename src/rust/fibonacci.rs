use std::env;

fn fibonacci(n: i32) {
    let mut a: u128 = 0;
    let mut b: u128 = 1;
    for _ in 0..n {
        print!("{} ", a);
        let temp = a;
        a = b;
        b = temp + b;
    }
    println!();
}

fn main() {
    let count_str = env::var("COUNT").unwrap_or("10".to_string());
    let count = count_str.parse::<i32>().unwrap_or(10);
    
    println!("Fibonacci Sequence (first {} numbers):", count);
    fibonacci(count);
}
