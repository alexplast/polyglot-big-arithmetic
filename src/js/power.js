const { performance } = require('perf_hooks');

const base = BigInt(parseInt(process.env.BASE) || 2);
const exp = parseInt(process.env.EXP) || 1000;

// Binary exponentiation for BigInt
function power(base, exp) {
    let result = 1n;
    let b = base;
    let e = exp;

    while (e > 0) {
        if (e % 2 === 1) {
            result *= b;
        }
        b *= b;
        e = Math.floor(e / 2);
    }

    return result;
}

const start = performance.now();
const result = power(base, exp);
const end = performance.now();

console.log(`Result(${base}^${exp}): ${result.toString()}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
