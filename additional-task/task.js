const isPrime = (n) => {
    if (n < 2) return false;
    for (let i = 2; i <= Math.sqrt(n); i++) {
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
            n = 0;
            currentNumber = 1;
        },

        iterate: async () => {
            currentNumber++;
            if (isPrime(currentNumber)) {
                n++;
                console.log(`Prime found: ${currentNumber}, count: ${n}`);
            }
            return n === target;
        },

        finalize: async () => {
            console.log(`Task completed! Found the ${target}th prime: ${currentNumber}`);
        },
    };
};

const runIterations = async (task, options, stats, batchStartTime) => {
    let batchIterations = 0;
    const { minDuration, maxDuration } = options;

    console.log("Starting new batch of iterations...");

    while (true) {
        const done = await task.iterate();
        stats.iterations++;
        batchIterations++;

        const elapsedTime = Date.now() - batchStartTime;
        console.log(
            `Iteration ${stats.iterations}, Batch iterations: ${batchIterations}, Elapsed time: ${elapsedTime}ms`
        );

        if (elapsedTime < minDuration) {
            console.log(`Waiting to meet minDuration of ${minDuration}ms...`);
            const waitTime = minDuration - elapsedTime;
            await new Promise(resolve => setTimeout(resolve, waitTime));
        }

        if (
            done ||
            batchIterations >= options.maxIterations ||
            elapsedTime >= maxDuration
        ) {
            if (done) console.log("Task finished during batch execution.");
            return done || elapsedTime >= maxDuration;
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

    return new Promise((resolve, reject) => {
        const timer = setTimeout(() => {
            console.error("Task timed out!");
            reject(new Error("Task timed out"));
        }, timeout);

        const execute = async () => {
            console.log("Executing task iterations...");

            const batchStartTime = Date.now();
            const done = await runIterations(task, options, stats, batchStartTime);

            if (done) {
                clearTimeout(timer);
                await task.finalize();
                resolve(`Task completed in ${stats.iterations} iterations.`);
                return;
            }

            if (stats.iterations < minIterations) {
                console.log("Not enough iterations, continuing immediately...");
                setTimeout(execute, 0);
            } else {
                console.log("Taking a short pause before next batch...");
                setTimeout(execute, 0);
            }
        };

        execute();
    });
};

(async () => {
    const task = createPrimeTask(100);

    try {
        const result = await asyncify(task, {
            minIterations: 5,
            maxIterations: 15,
            minDuration: 20,
            maxDuration: 100,
            timeout: 30,
        });
        console.log(result);
    } catch (error) {
        console.error("Error:", error.message);
    }
})();
