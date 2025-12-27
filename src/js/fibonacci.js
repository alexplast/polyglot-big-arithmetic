function fibonacci(n) {
    let a = 0n, b = 1n;
    for (let i = 0; i < n; i++) {
        process.stdout.write(a + " ");
        let temp = a;
        a = b;
        b = temp + b;
    }
}

const count = parseInt(process.env.COUNT || '10');
console.log(`Fibonacci Sequence (first ${count} numbers):`);
fibonacci(count);
