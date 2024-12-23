# Reactive message-based communication between entities

import asyncio

class EventEmitter:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def emit(self, message):
        await self.queue.put(message)

    async def subscribe(self):
        while True:
            message = await self.queue.get()
            if message is None:
                break
            yield message


async def async_data_source(emitter):
    data = ([1, 2, "error1", 3, 4, 5, 6, "error3"] + list(range(7, 101))) * 5
    for item in data:
        await emitter.emit(item)
        await asyncio.sleep(0.01)
    await emitter.emit(None)


async def is_even(num):
    await asyncio.sleep(0.01)
    if not isinstance(num, int):
        raise TypeError(f"Expected an integer, got {type(num).__name__}")
    return num % 2 == 0


async def async_filter(func, emitter, cancel_event):
    filtered_items = []

    async for item in emitter.subscribe():
        if cancel_event.is_set():
            print("Cancel event detected. Stopping data processing.")
            break

        try:
            if await func(item):
                filtered_items.append(item)
        except Exception as e:
            print(f"Error while processing item '{item}': {e}")

    return filtered_items


async def process_data():
    cancel_event = asyncio.Event()
    emitter = EventEmitter()

    data_source_task = asyncio.create_task(async_data_source(emitter))

    try:
        filtered_data = await async_filter(is_even, emitter, cancel_event)
        print(f"\nFiltered data: {filtered_data}\n")
    except asyncio.CancelledError:
        print("Processing was canceled.")
    finally:
        await data_source_task


async def main():
    print("Task 5: Reactive message-based communication between entities\n")
    await process_data()


if __name__ == "__main__":
    asyncio.run(main())
