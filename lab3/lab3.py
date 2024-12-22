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
            abort_controller.cancel()
            for _, t in tasks:
                if not t.done():
                    t.cancel()
            raise e
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
    return (num & (num - 1)) == 0


async def is_even(num):
    await asyncio.sleep(0.05)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0


async def main():
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
        print("Uppercase strings in list1:", results[0])
        print("Powers of two in list2:", results[1])
        print("Even numbers in list3:", results[2])
    except asyncio.CancelledError:
        print("The operation has been canceled.")
        raise


if __name__ == "__main__":
    asyncio.run(main())
