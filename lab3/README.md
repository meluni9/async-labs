# Lab 3: AbortController and Cancellation
## Description:
In this lab, you need to implement `AbortController` or other approach for canceling asynchronous operations.
## Implementation:
### [lab3.py](./lab3.py): Cancellation implementation.
```python
import asyncio

async def async_filter(func, arr, cancel_event):
    print("Processing data...")
    tasks = []
    for item in arr:
        if cancel_event.is_set():
            print("Cancel event detected. Stopping further tasks.")
            break
        task = asyncio.create_task(func(item))
        tasks.append((item, task))

    results = []
    for item, task in tasks:
        try:
            result = await task
            if result:
                results.append(item)
        except Exception as e:
            print(f"{e} error encountered, cancelling further tasks in current list operation...")
            cancel_event.set()
            for _, t in tasks:
                if not t.done():
                    t.cancel()
            await asyncio.gather(*[t for _, t in tasks], return_exceptions=True)
            raise
    return results

async def is_upper(word):
    await asyncio.sleep(0.1)
    if not isinstance(word, str):
        raise TypeError(f"Expected a string, got {type(word).__name__}")
    return word.isupper()

async def is_two_power(num):
    await asyncio.sleep(0.2)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    elif num <= 0:
        raise ValueError(f"Expected a positive integer, got {num}")
    return (num & (num - 1)) == 0

async def is_even(num):
    await asyncio.sleep(0.5)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0

async def process_all_asynchronously(cancel_event):
    list1 = ['KPI', 'Kpi', 'KPI', 'kpI', 'kPi', 'KPI']
    list2 = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, 'e', 8]
    tasks = [
        asyncio.create_task(async_filter(is_upper, list1, cancel_event)),
        asyncio.create_task(async_filter(is_two_power, list2, cancel_event)),
        asyncio.create_task(async_filter(is_even, list3, cancel_event)),
    ]
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print("\nProcessing results:")
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                print(f"Task {i} failed: {result}")
            else:
                print(f"Task {i} result: {result}")
    except asyncio.CancelledError:
        print("Tasks have been canceled.")

async def main():
    print("Task 3: Integration of Cancellable approach\n")
    cancel_event = asyncio.Event()
    task = asyncio.create_task(process_all_asynchronously(cancel_event))
    try:
        await asyncio.sleep(1.5)
        cancel_event.set()
        await task
    except asyncio.CancelledError:
        print("The main task has been canceled gracefully.")

if __name__ == "__main__":
    asyncio.run(main())
```
### [lab3_abort_controller.py](./lab3_abort_controller.py): Implementation of canceling asynchronous operations using AbortController.
```python
import asyncio

class AbortController:
    def __init__(self):
        self._cancel_event = asyncio.Event()

    def cancel(self):
        self._cancel_event.set()

    async def wait_for_cancel(self):
        await self._cancel_event.wait()

    def is_cancelled(self):
        return self._cancel_event.is_set()

async def async_filter(func, arr, abort_controller):
    print("Processing data...")
    tasks = []
    for item in arr:
        task = asyncio.create_task(func(item))
        tasks.append((item, task))

    results = []
    for item, task in tasks:
        try:
            result = await task
            if result:
                results.append(item)
        except Exception as e:
            print(f"{e} error encountered, cancelling further tasks in current list operation...")
            abort_controller.cancel()
            for _, t in tasks:
                if not t.done():
                    t.cancel()
            await asyncio.gather(*[t for _, t in tasks], return_exceptions=True)
            raise
    return results

async def is_upper(word):
    await asyncio.sleep(0.1)
    if not isinstance(word, str):
        raise TypeError(f"Expected a string, got {type(word).__name__}")
    return word.isupper()

async def is_two_power(num):
    await asyncio.sleep(0.2)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    elif num <= 0:
        raise ValueError(f"Expected a positive integer, got {num}")
    return (num & (num - 1)) == 0

async def is_even(num):
    await asyncio.sleep(0.5)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0

async def process_all_asynchronously():
    list1 = ['KPI', 'Kpi', 'KPI', 'kpI', 'kPi', 'KPI']
    list2 = [-1, 0, 1, 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, 'e', 8]
    abort_controller1 = AbortController()
    abort_controller2 = AbortController()
    abort_controller3 = AbortController()
    tasks = [
        asyncio.create_task(async_filter(is_upper, list1, abort_controller1)),
        asyncio.create_task(async_filter(is_two_power, list2, abort_controller2)),
        asyncio.create_task(async_filter(is_even, list3, abort_controller3)),
    ]
    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        print("\nProcessing results:")
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                print(f"Task {i} failed: {result}")
            else:
                print(f"Task {i} result: {result}")
    except asyncio.CancelledError:
        print("Tasks have been canceled.")

async def main():
    print("Task 3: Integration of AbortController\n")
    task = asyncio.create_task(process_all_asynchronously())
    abort_controller = AbortController()
    try:
        await asyncio.sleep(1.5)
        abort_controller.cancel()
        await task
    except asyncio.CancelledError:
        print("The main task has been canceled gracefully.")

if __name__ == "__main__":
    asyncio.run(main())
```
## Testing program

### Test 1
<img src="./media/lab_1_test_1.png">

### Test 2
<img src="./media/lab_1_test_2.png">

### Test 3
<img src="./media/lab_1_test_3.png">
