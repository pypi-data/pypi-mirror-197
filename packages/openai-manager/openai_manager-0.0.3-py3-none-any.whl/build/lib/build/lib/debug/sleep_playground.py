import asyncio


async def submit_something():
    print("Hello!")
    await asyncio.sleep(1)  # hand over control!
    print("World!")


async def main():
    task_lst = [asyncio.create_task(submit_something()) for _ in range(10)]
    return await asyncio.gather(*task_lst)

# run this main()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
