# Task 4: Ongoing processing of large data sets that do not fit in memory

import asyncio

async def async_data_source(batch_size=20):
    data = range(1, 1001)
    chunk = []
    for idx, item in enumerate(data, start=1):
        chunk.append(item)
        if len(chunk) == batch_size:
            yield chunk
            await asyncio.sleep(0.5)
            chunk = []
    if chunk:
        yield chunk


async def async_process_chunk(chunk):
    print(f"Processing chunk: {chunk}")
    await asyncio.sleep(2)
    return [item * 2 for item in chunk]


async def process_large_data():
    async for chunk in async_data_source(15):
        processed_data = await async_process_chunk(chunk)
        print(f"Processed data: {processed_data}\n")


async def main():
    print("Task 4: Ongoing processing of large data sets that do not fit in memory")
    task = asyncio.create_task(process_large_data())

    try:
        await task
    except asyncio.CancelledError:
        print("The main task has been canceled gracefully.")

if __name__ == "__main__":
    asyncio.run(main())
