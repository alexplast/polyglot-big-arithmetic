const count = parseInt(process.env.COUNT) || 10;

let a = 0n;
let b = 1n;

for (let i = 0; i < count; i++) {
    let temp = a;
    a = b;
    b = temp + b;
}

console.log(`Result(F_${count}): ${a.toString()}`);
