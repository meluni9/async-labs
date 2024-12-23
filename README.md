# Async Labs

This repository contains labs from the subject Components of Software Engineering. Part 2. Software Modeling. Software Requirements Analysis.

This repository contains various tasks designed to demonstrate asynchronous programming concepts using Python. Each task focuses on different aspects of concurrency, parallelism, and reactive programming. Below is a description of each lab and links to the relevant files for each task.

## Lab Assignments

- [Lab 1](./lab1/)
- [Lab 2](./lab2/)
- [Lab 3](./lab3/)
- [Lab 4](./lab4/)
- [Lab 5](./lab5/)

## All tasks adaptation for python

  Task 0
  * Prepare GitHub repo for Tasks
  * Prepare synchronous adaptation for Task 1

  Task 1
  * Choose array fn (map/filter/filterMap/some/find/findIndex) -> chosen ```filter``` fn 
  * Prepare its callback based async counterpart
  * Prepare demo cases for the usage
  * Add new on-demand feature during review e.g.: Add support for debounce (if the task took less then X time to
    complete - add an execution delay)

  Task 2
  * Write use cases for the async-await
  * Add new on-demand feature during review
    e.g.: Add support for parallelism

  Task 3
  * Integrate AbortController or other Cancellable approach

  Task 4 
  * Stream/AsyncIterator/Alternative
  * Ongoing processing of large data sets that do not fit in memory

  Task 5 
  * Observable/EventEmitter/Alternative
  * Reactive message based on communication between entities

## Repository Structure
```
async-labs
|- lab1
|  |- lab0.py
|  |- lab1.py
|  |- lab1_debounce.py
|  |- README.md
|- lab2
|  |- lab2.py
|  |- README.md
|- lab3
|  |- lab3.py
|  |- lab3_abort_controller.py
|  |- README.md
|- lab4
|  |- lab4_generator.py
|  |- lab4_chunks.py
|  |- README.md
|- lab5
|  |- lab5.py
|  |- README.md
|- README.md
```

Each subdirectory contains a `README.md` file with specific details about the task, the approach taken, and usage instructions.
## How to Run
1. Clone this repository.
2. Navigate to the relevant lab directory.
3. Execute the Python file(s) using the `python` command, e.g., `python lab1.py`.
