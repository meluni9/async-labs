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

const runIterations = (task, options) => {
    const { maxIterations = 10 } = options;
    const startTime = Date.now();

    for (let i = 0; i < maxIterations; i++) {
        const done = task.iterate();
        if (done) return true;

        const elapsed = Date.now() - startTime;
        console.log(`Iteration ${i + 1}, elapsed time: ${elapsed}ms`);
    }
    return false;
};


const asyncify = (task, options) => {
    task.init();

    const execute = () => {
        const completed = runIterations(task, options);
        if (completed) {
            console.log("Task completed!");
        } else {
            console.log("Continuing task...");
            setTimeout(execute, 0);
        }
    };

    execute();
};

const testTask = createPrimeTask(5);
testTask.init();

let iterations = 0;
while (!testTask.iterate()) {
    iterations++;
    if (iterations > 100) {
        console.log("Not enough iterations");
        break;
    }
}
testTask.finalize();

const asyncTask = createPrimeTask(10);
asyncify(asyncTask, { maxIterations: 5 });
