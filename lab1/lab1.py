# Task 1: Prepare filter callback based async counterpart
# Prepare demo cases for the usage
# Add support for debounce (if the task took less then X time to complete - add an execution delay)

import asyncio

async def async_filter(func, arr):
    result = []
    print(f"Processing data with delay...")
    for item in arr:
        if await func(item):
            result.append(item)
    return result


async def is_upper(word):
    await asyncio.sleep(0.1)
    return type(word) is str and word.isupper()


async def is_two_power(num):
    await asyncio.sleep(0.2)
    if type(num) is not int or num <= 0:
        return False
    return (num & (num - 1)) == 0


async def is_even(num):
    await asyncio.sleep(0.05)
    return type(num) is int and num % 2 == 0


async def main():
    list1 = ['KPI', 'Kpi', 2, 'KPI', 'kpI', (3, 4), 'kPi', 'KPI']
    list2 = [-1, 0, 1, 'e', 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, (3, 'e'), 8]

    print("Task 1: Sequential Filtering")
    print("Filtering uppercase strings from list1:")
    print(await async_filter(is_upper, list1))
    print("Filtering powers of two from list2:")
    print(await async_filter(is_two_power, list2))
    print("Filtering even numbers from list3:")
    print(await async_filter(is_even, list3))


asyncio.run(main())
