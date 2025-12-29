const { performance } = require('perf_hooks');

const base = parseFloat(process.env.BASE) || 2.0;
const exp = parseInt(process.env.EXP) || 1023;

const start = performance.now();
const result = Math.pow(base, exp);
const end = performance.now();

console.log(`Result(${base}^${exp}): ${result.toExponential(10)}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
