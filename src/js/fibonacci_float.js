const { performance } = require('perf_hooks');
const count = parseInt(process.env.COUNT) || 1475;

let a = 0.0;
let b = 1.0;

const start = performance.now();
for (let i = 0; i < count; i++) {
    let temp = a;
    a = b;
    b = temp + b;
}
const end = performance.now();

console.log(`Result(F_${count}): ${a.toExponential(10)}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
