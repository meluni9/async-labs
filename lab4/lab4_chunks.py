# Task 4: Ongoing processing of large data sets that do not fit in memory in chunks

import asyncio

async def async_data_source(batch_size=20):
    data = range(1, 1001)
    chunk = ['e']
    for idx, item in enumerate(data, start=1):
        chunk.append(item)
        if len(chunk) == batch_size:
            yield chunk
            await asyncio.sleep(0.2)
            chunk = []
    if chunk:
        yield chunk


async def async_filter_chunk(func, chunk, cancel_event):
    if cancel_event.is_set():
        print("Cancel event detected. Skipping this chunk.")
        return []

    tasks = [asyncio.create_task(func(item)) for item in chunk]
    filtered_items = []

    for item, task in zip(chunk, tasks):
        try:
            result = await task
            if result:
                filtered_items.append(item)
        except Exception as e:
            print(f"Error while processing item {item}: {e}. Skipping remaining items in chunk.\n")
            # cancel_event.set()  # Stop further chunk processing globally
            break

    for task in tasks:
        if not task.done():
            task.cancel()

    return filtered_items


async def is_even(num):
    await asyncio.sleep(0.1)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0


async def process_large_data(cancel_event):
    async for chunk in async_data_source(15):
        if cancel_event.is_set():
            print("Cancel event detected. Stopping data processing.")
            break

        print(f"Received chunk: {chunk}")
        filtered_chunk = await async_filter_chunk(is_even, chunk, cancel_event)
        if filtered_chunk:
            print(f"Filtered chunk: {filtered_chunk}\n")

    print("Data processing completed.\n")


async def main():
    print("Task 4: Large dataset processing with chunk-level error handling\n")
    cancel_event = asyncio.Event()
    task = asyncio.create_task(process_large_data(cancel_event))

    try:
        await task
    except asyncio.CancelledError:
        print("The main task has been canceled gracefully.")


if __name__ == "__main__":
    asyncio.run(main())
