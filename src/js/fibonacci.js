const { performance } = require('perf_hooks');
const count = parseInt(process.env.COUNT) || 10;

let a = 0n;
let b = 1n;

const start = performance.now();
for (let i = 0; i < count; i++) {
    let temp = a;
    a = b;
    b = temp + b;
}
const end = performance.now();

console.log(`Result(F_${count}): ${a.toString()}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
