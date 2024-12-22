import asyncio


async def parallel_filter(func, arr):
    tasks = []
    print(f"Processing data...")
    for item in arr:
        tasks.append(asyncio.create_task(func(item)))
    results = await asyncio.gather(*tasks)
    return [item for item, result in zip(arr, results) if result]

async def async_filter(func, arr):
    result = []
    print(f"Processing data...")
    for item in arr:
        if await func(item):
            result.append(item)
    return result


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

    print("Task 2: Parallel filtering with asyncio")

    print("\nFiltering uppercase strings from list1:")
    print(await parallel_filter(is_upper, list1))

    print("\nFiltering powers of two from list2:")
    print(await parallel_filter(is_two_power, list2))

    print("\nFiltering even numbers from list3:")
    print(await parallel_filter(is_even, list3))


if __name__ == "__main__":
    asyncio.run(main())
