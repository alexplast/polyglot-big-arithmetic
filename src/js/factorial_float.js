const { performance } = require('perf_hooks');
const count = parseInt(process.env.COUNT) || 170;

let factorial = 1.0;

const start = performance.now();
for (let i = 1; i <= count; i++) {
    factorial *= i;
}
const end = performance.now();

console.log(`Result(${count}!): ${factorial.toExponential(10)}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
