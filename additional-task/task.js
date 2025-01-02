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

(async () => {
  const task = createPrimeTask(100);
  const options = { minIterations: 5, maxIterations: 10, timeout: 30 };

  try {
    await asyncify(task, options);
  } catch (error) {
    console.error("Error:", error.message);
  }
})();
