# Task 4: Ongoing processing of large data sets with async_filter using generator

import asyncio

async def async_data_source():
    data = [1, 2, "error1", 3, 4, "error2", 5, 6, "error3"] + list(range(7, 101))
    for item in data:
        yield item
        await asyncio.sleep(0.01)


async def async_filter(func, cancel_event):
    filtered_items = []
    async for item in async_data_source():
        if cancel_event.is_set():
            print("Cancel event detected. Stopping data processing.")
            break

        try:
            if await func(item):
                filtered_items.append(item)
        except Exception as e:
            print(f"Error while processing item '{item}': {e}")

    return filtered_items


async def is_even(num):
    await asyncio.sleep(0.01)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0


async def process_data(cancel_event):
    print("Processing data...\n")
    filtered_data = await async_filter(is_even, cancel_event)
    print(f"Filtered data: {filtered_data}\n")


async def main():
    print("Task 4: Large dataset processing with error handling\n")
    cancel_event = asyncio.Event()
    task = asyncio.create_task(process_data(cancel_event))

    try:
        await task
    except asyncio.CancelledError:
        print("The main task has been canceled gracefully.")


if __name__ == "__main__":
    asyncio.run(main())
