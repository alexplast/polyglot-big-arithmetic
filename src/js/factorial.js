const { performance } = require('perf_hooks');
const count = parseInt(process.env.COUNT) || 200;

// console.log(`Calculating Factorial(${count})...`);

let factorial = 1n; // Use BigInt

const start = performance.now();
for (let i = 1; i <= count; i++) {
    factorial *= BigInt(i);
}
const end = performance.now();

console.log(`Result(${count}!): ${factorial.toString()}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
