const fs = require('fs');
const { performance } = require('perf_hooks');

const N = parseInt(process.env.SORT_SIZE) || 10000;

let buffer;
try {
    buffer = fs.readFileSync('data.bin');
} catch (e) {
    console.error("Error: 'data.bin' not found. Run 'python3 tests/gen_data.py' first.");
    process.exit(1);
}

if (buffer.length < N * 8) {
    console.warn(`Warning: data.bin has ${buffer.length} bytes, need ${N * 8}. Reading what works.`);
}

// Node.js Buffers are Uint8Array. 
// We create a Float64Array view on top of the binary data.
// Note: This assumes the system is Little Endian (standard for x64/ARM).
// If running on Big Endian hardware, this requires manual swapping.
const elementCount = Math.floor(buffer.length / 8);
const limit = Math.min(N, elementCount);

// Copy to ensure we have a writable array of the correct size N (filled with 0s if file short)
const arr = new Float64Array(N);
const fileView = new Float64Array(buffer.buffer, buffer.byteOffset, limit);
arr.set(fileView);

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
let pLimit = (N < 5) ? N : 5;
for(let i=0; i<pLimit; i++) out += arr[i].toFixed(4) + " ";
out += "... ";
if (N > 5) {
    for(let i=N-5; i<N; i++) out += arr[i].toFixed(4) + " ";
}
console.log(out);

console.log(`Time: ${(end - start).toFixed(3)} ms`);
