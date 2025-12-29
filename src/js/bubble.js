const { performance } = require('perf_hooks');
const N = parseInt(process.env.SORT_SIZE) || 10000;

const arr = new Float64Array(N);
let seed = 42;

// Simple LCG emulation
for (let i = 0; i < N; i++) {
    seed = (seed * 1664525 + 1013904223) >>> 0; // Force 32-bit unsigned
    arr[i] = seed / 4294967296.0;
}

const start = performance.now();
for (let i = 0; i < N - 1; i++) {
    for (let j = 0; j < N - i - 1; j++) {
        if (arr[j] > arr[j+1]) {
            let temp = arr[j];
            arr[j] = arr[j+1];
            arr[j+1] = temp;
        }
    }
}
const end = performance.now();

let out = `Sort(${N}): `;
for(let i=0; i<5; i++) out += arr[i].toFixed(4) + " ";
out += "... ";
for(let i=N-5; i<N; i++) out += arr[i].toFixed(4) + " ";
console.log(out);

console.log(`Time: ${(end - start).toFixed(3)} ms`);
