const isPrime = (n) => {
    if (n < 2) return false;
    for (let i = 2; i <= n - 1; i++) {
        if (n % i === 0) return false;
    }
    return true;
};

const createPrimeTask = (target) => {
    let n = 0;
    let currentNumber = 1;

    return {
        init: () => {
            console.log("Task initialized");
        },

        iterate: () => {
            currentNumber++;
            if (isPrime(currentNumber)) {
                n++;
                console.log(`Prime found: ${currentNumber}, count: ${n}`);
            }
            return n === target;
        },

        finalize: () => {
            console.log(`Task completed! Found the ${target}th prime: ${currentNumber}`);
        },
    };
};

const task = createPrimeTask(3);

task.init();

let isDone = false;
while (!isDone) {
    isDone = task.iterate();
}

task.finalize();
