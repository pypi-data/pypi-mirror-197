import asyncio
import time
import aiohttp

def simple_func():
    q = asyncio.Queue()
    

# test if appending async objects to list are blocking...
async def run_thread(tid=-1):
    print(f"running thread {tid}...")
    await asyncio.sleep(1)  # mimick IO operation
    # time.sleep(1)
    print(f"complete thread {tid}...")
    return "Hello"

async def run_crawl(url="http://mrxiao.net", session=None, i=-1):
    print(f"running crawl thread {url}...")
    assert session is not None
    # async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        response = await response.text()
        print(f"response {i}: {response}")
        return response

# 结论：可以实现存着future的list，然后await gather(*list)来等待所有的future完成；
async def main():
    task_lst = []
    session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1))
    for i in range(50):
        # task = asyncio.create_task(run_thread(i))
        # async with aiohttp.ClientSession() as session:
        task = asyncio.create_task(run_crawl(session=session, i=i))
        task_lst.append(task)
    
    return await asyncio.gather(*task_lst)

async def print_something(s):
    print('in print_someting')
    asyncio.sleep(3)
    print(s)

async def create_task_but_not_await_it():
    task = asyncio.create_task(print_something('Hello'))
    task2 = asyncio.create_task(print_something('World'))
    asyncio.sleep(3)  # give up control to see if print_something works -> it works
    print("Done")
    # task will be executed even if no one awaits it
    # time.sleep(1)  # blocking it!


loop = asyncio.get_event_loop()
task = loop.run_until_complete(create_task_but_not_await_it())

print(task)
