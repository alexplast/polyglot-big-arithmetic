const { performance } = require('perf_hooks');

const N = parseInt(process.env.MATRIX_SIZE) || 256;

// TypedArray is closer to "Native" C arrays than standard JS Arrays
const A = new Float64Array(N * N);
const B = new Float64Array(N * N);
const C = new Float64Array(N * N);

for (let i = 0; i < N * N; i++) {
    A[i] = 1.0 + (i % 100) * 0.01;
    B[i] = 1.0 - (i % 100) * 0.01;
}

const start = performance.now();

for (let i = 0; i < N; i++) {
    for (let k = 0; k < N; k++) {
        const r = A[i * N + k];
        const rowC = i * N;
        const rowB = k * N;
        for (let j = 0; j < N; j++) {
            C[rowC + j] += r * B[rowB + j];
        }
    }
}

const end = performance.now();

console.log(`Matrix(${N}x${N})`);
console.log(`Result[0]: ${C[0]}`);
console.log(`Time: ${(end - start).toFixed(3)} ms`);
