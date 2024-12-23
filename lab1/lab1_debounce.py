# Add support for debounce (if the task took less then X time to complete - add an execution delay)

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
