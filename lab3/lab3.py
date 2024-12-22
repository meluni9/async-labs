import asyncio


async def async_filter(func, arr):
    tasks = []
    print("Processing data...")

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
            print(f"Error processing item {item}: {e}")

    return results


async def is_upper(word):
    try:
        await asyncio.sleep(0.1)
        if not isinstance(word, str):
            raise ValueError("Expected a string")
        return word.isupper()
    except asyncio.CancelledError:
        print(f"is_upper task for '{word}' was cancelled.")
        raise


async def is_two_power(num):
    try:
        await asyncio.sleep(0.2)
        if not isinstance(num, int):
            raise ValueError("Expected an integer")
        if num <= 0:
            return False
        return (num & (num - 1)) == 0
    except asyncio.CancelledError:
        print(f"is_two_power task for '{num}' was cancelled.")
        raise


async def is_even(num):
    try:
        await asyncio.sleep(0.05)
        if not isinstance(num, int):
            raise ValueError("Expected an integer")
        return num % 2 == 0
    except asyncio.CancelledError:
        print(f"is_even task for '{num}' was cancelled.")
        raise


async def main():
    list1 = ['KPI', 'Kpi', 2, 'KPI', 'kpI', (3, 4), 'kPi', 'KPI']
    list2 = [-1, 0, 1, 'e', 2, 3, 4, 5, 6, 7, 'b', 8, 9, 10]
    list3 = [3, 5, 6, (3, 'e'), 8]

    tasks = [
        asyncio.create_task(async_filter(is_upper, list1)),
        asyncio.create_task(async_filter(is_two_power, list2)),
        asyncio.create_task(async_filter(is_even, list3)),
    ]

    try:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Task {i + 1} encountered an exception: {result}")
            else:
                print(f"Result of task {i + 1}: {result}")
    except asyncio.CancelledError:
        print("Main task was cancelled.")


if __name__ == "__main__":
    asyncio.run(main())
