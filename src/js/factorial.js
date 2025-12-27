const count = parseInt(process.env.COUNT) || 200;

// console.log(`Calculating Factorial(${count})...`);

let factorial = 1n; // Use BigInt

for (let i = 1; i <= count; i++) {
    factorial *= BigInt(i);
}

console.log(`Result(${count}!): ${factorial.toString()}`);
