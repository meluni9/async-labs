[🏠 Home Page](../) | [📝 Lab 1_2](/) | [📝 Lab 3](../lab3/) | [📝 Lab 4](../lab4/) | [📝 Lab 5](../lab5/) | [📝 Additional task](../additional-task/) 

# Additional task

## Description:
This project provides a solution to asynchronously compute prime numbers using an efficient event loop-friendly approach in Node.js. The code divides the computation into manageable iterations to prevent blocking the Node.js event loop and ensure smooth handling of other tasks.

## Features

- Calculates prime numbers up to a specified target count.
- Prevents blocking the event loop using asynchronous iteration.
- Configurable iteration and timeout options.
- Logs progress and execution statistics in real time.

## Implementation:

### [task.js](./lab1_2.py): The script computes the nth prime number asynchronously. You can configure the parameters for iteration and timeout to suit your needs.
Implements parallel filtering using `asyncio.gather`. Demonstrates use cases for async/await patterns.
```js
const isPrime = (n) => {
    if (n < 2) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
        if (n % i === 0) return false;
    }
    return true;
};

const createPrimeTask = (target) => {
    let primeCount = 0;
    let currentNumber = 1;

    return {
        init: () => {
            console.log("Task initialized");
            primeCount = 0;
            currentNumber = 1;
        },

        iterate: async () => {
            while (++currentNumber) {
                if (isPrime(currentNumber)) {
                    primeCount++;
                    console.log(`Prime found: ${currentNumber}, count: ${primeCount}`);
                    return primeCount === target;
                }
            }
        },

        finalize: async () => {
            console.log(`Task completed! Found the ${target}th prime: ${currentNumber}`);
        },
    };
};

const runIterations = async (task, options, stats, batchStartTime) => {
    const { maxIterations, maxDuration } = options;
    let batchIterations = 0;

    console.log("Starting new batch of iterations...");

    while (true) {
        const done = await task.iterate();
        stats.iterations++;
        batchIterations++;

        const elapsedTime = Date.now() - batchStartTime;
        console.log(
            `Iteration ${stats.iterations}, Batch iterations: ${batchIterations}, Elapsed time: ${elapsedTime}ms`
        );

        if (done) {
            console.log("Task finished during batch execution.");
            return true;
        }

        if (batchIterations >= maxIterations || elapsedTime >= maxDuration) {
            console.log("Batch limit reached (iterations or duration).");
            return false;
        }
    }
};

const asyncify = async (task, options) => {
    const {
        minIterations = 5,
        maxIterations = 10,
        minDuration = 1000,
        maxDuration = 60000,
        timeout = 60000,
    } = options;

    const stats = { iterations: 0 };

    await task.init();

    console.log("Asyncify started with options:", options);

    return new Promise(async (resolve, reject) => {
        const timer = setTimeout(() => {
            console.error("Task timed out!");
            reject(new Error("Task timed out"));
        }, timeout);

        const execute = async () => {
            const batchStartTime = Date.now();
            const done = await runIterations(task, options, stats, batchStartTime);

            if (done) {
                clearTimeout(timer);
                await task.finalize();
                resolve(`Task completed in ${stats.iterations} iterations.`);
                return;
            }

            const elapsedTime = Date.now() - batchStartTime;
            if (stats.iterations < minIterations || elapsedTime < minDuration) {
                console.log("Minimum iterations or duration not yet met, continuing immediately...");
                setTimeout(execute, 0);
            } else {
                console.log("Taking a short pause before next batch...");
                setTimeout(execute, 50);
            }
        };

        await execute();
    });
};

(async () => {
    const task = createPrimeTask(100);

    try {
        const result = await asyncify(task, {
            minIterations: 5,
            maxIterations: 15,
            minDuration: 1,
            maxDuration: 7,
            timeout: 10000,
        });
        console.log(result);
    } catch (error) {
        console.error("Error:", error.message);
    }
})();
```
