[🏠 Home Page](../) | [📝 Lab 1](../lab1/) | [📝 Lab 2](../lab2/) | [📝 Lab 3](../lab3/) | [📝 Lab 4](../lab4/) | [📝 Lab 5](../lab5/)

# Lab 1: Asynchronous Alternative for Filter function
## Description:
In this lab, you need to choose one of the array functions (e.g., `map`, `filter`, `find`, etc.) and develop an asynchronous version of this function, demonstrate showcases and add support for debounce.
## Implementation:

### [lab0.py](./lab0.py): Example use cases for synchronous filter function.
Demonstrates a synchronous implementation of a filter function with example cases such as filtering uppercase strings, powers of two, and even numbers.
```python
def sync_filter(func, arr):
    return [item for item in arr if func(item)]

def is_upper(word):
    return isinstance(word, str) and word.isupper()

def is_two_power(num):
    if not isinstance(num, int) or num <= 0:
        return False
    return (num & (num - 1)) == 0

def is_even(num):
    return isinstance(num, int) and num % 2 == 0

def main():
    list1 = ['KPI', 'Kpi', 2, 'KPI', 'kpI', (3, 4), 'kPi', 'KPI']
    list2 = [-1, 0, 1, 'e', 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, (3, 'e'), 8]

    print("Task 0: Synchronous filtering")
    print("\nUppercase strings in list1:")
    print(sync_filter(is_upper, list1))

    print("\nPowers of two in list2:")
    print(sync_filter(is_two_power, list2))

    print("\nEven numbers in list3:")
    print(sync_filter(is_even, list3))

if __name__ == "__main__":
    main()
```

### [lab1.py](./lab1.py): Implementation of the asynchronous counterpart for filter functions.
Uses async/await for asynchronous operations.
```python
import asyncio

async def async_filter(func, arr):
    return [item for item in arr if await func(item)]

async def is_upper(word):
    await asyncio.sleep(0.1)
    return isinstance(word, str) and word.isupper()

async def is_two_power(num):
    await asyncio.sleep(0.2)
    if not isinstance(num, int) or num <= 0:
        return False
    return (num & (num - 1)) == 0

async def is_even(num):
    await asyncio.sleep(0.05)
    return isinstance(num, int) and num % 2 == 0

async def main():
    list1 = ['KPI', 'Kpi', 2, 'KPI', 'kpI', (3, 4), 'kPi', 'KPI']
    list2 = [-1, 0, 1, 'e', 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, (3, 'e'), 8]

    print("Task 1: Sequential filtering without debounce")
    print("\nUppercase strings in list1:")
    print(await async_filter(is_upper, list1))

    print("\nPowers of two in list2:")
    print(await async_filter(is_two_power, list2))

    print("\nEven numbers in list3:")
    print(await async_filter(is_even, list3))

if __name__ == "__main__":
    asyncio.run(main())
```

### [lab1_debounce.py](./lab1_debounce.py): Demonstration of adding debounce (delay) to asynchronous execution.
Has a debounce support, which adds extra delay if the execution time is less than a specified limit.
```python
import asyncio
from time import perf_counter

async def async_filter(func, arr, debounce_time=0.1):
    result = []
    for item in arr:
        start_time = perf_counter()
        if await func(item):
            result.append(item)
        # Add debounce if the task completed too quickly
        elapsed_time = perf_counter() - start_time
        if elapsed_time < debounce_time:
            await asyncio.sleep(debounce_time - elapsed_time)
    return result

async def is_upper(word):
    await asyncio.sleep(0.09)
    return isinstance(word, str) and word.isupper()

async def is_two_power(num):
    await asyncio.sleep(0.15)
    if not isinstance(num, int) or num <= 0:
        return False
    return (num & (num - 1)) == 0

async def is_even(num):
    await asyncio.sleep(0.05)
    return isinstance(num, int) and num % 2 == 0

async def main():
    list1 = ['KPI', 'Kpi', 2, 'KPI', 'kpI', (3, 4), 'kPi', 'KPI']
    list2 = [-1, 0, 1, 'e', 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, (3, 'e'), 8]

    print("Task 1: Sequential filtering with debounce")
    print("\nUppercase strings in list1:")
    print(await async_filter(is_upper, list1, debounce_time=0.1))

    print("\nPowers of two in list2:")
    print(await async_filter(is_two_power, list2, debounce_time=0.2))

    print("\nEven numbers in list3:", )
    print(await async_filter(is_even, list3, debounce_time=0.1))

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

