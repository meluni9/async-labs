# Task 4: Ongoing processing of large data sets with async_filter using generator

import asyncio


async def async_generator_filter(func, items, cancel_event):
    for item in items:
        if cancel_event.is_set():
            raise asyncio.CancelledError("Task was cancelled")
        try:
            if await func(item):
                yield item
        except Exception as e:
            raise Exception(f"Error processing item {item} ({e})")


async def is_even(num):
    await asyncio.sleep(0.1)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0


async def process_all_asynchronously(cancel_event):
    data = [1, 2, 3, 4] * 10 + ['d'] + [5, 6, 7, 8] * 10
    try:
        async for filtered_item in async_generator_filter(is_even, data, cancel_event):
            print(f"Filtered item: {filtered_item}")
    except asyncio.CancelledError:
        print("Processing was cancelled.")
    except Exception as e:
        print(f"Error encountered: {e}")


async def main():
    cancel_event = asyncio.Event()
    task = asyncio.create_task(process_all_asynchronously(cancel_event))

    try:
        await task
    except asyncio.CancelledError:
        print("The main task has been cancelled gracefully.")


if __name__ == "__main__":
    asyncio.run(main())
