import asyncio
import functools

async def test():
    for i in range(2):
        await asyncio.sleep(0)
        print("-"*20)
    return "t1"
        
async def test2():
    for i in range(5):
        await asyncio.sleep(0)
        print("*"*20)
    return "t2"


def callback(task:asyncio.Task, num):
    print(f"{task.get_coro()} is done{num}...")




async def main():

    # #直接await，但是不能并发:coroutine 'test2' was never awaited
    # rst = await test(), test2()
    # print(rst)

    # #gather函数
    # rst = await asyncio.gather(test(), test2())
    # print(rst)


    #使用task类
    t1 = asyncio.create_task(test())
    t2 = asyncio.create_task(test2())
    #await t1, t2
    # print(f"{t1.result()=}, {t2.result()=}")

    #添加回调函数
    # t1.add_done_callback(callback)
    # t2.add_done_callback(callback)

    #添加带返回值的回调函数
    def my_partial(func, /, *args, **kwargs):
        def wrap(*warp_args, **warp_kwargs):
            merged_kwrags = {**kwargs, **warp_kwargs}
            return func(*args, *warp_args, **merged_kwrags)
        return wrap

    n_callback = functools.partial(callback, num=3,)
    # n_callback = my_partial(callback, num=3)
    t1.add_done_callback(n_callback)
    t2.add_done_callback(n_callback)

    done, pending = await asyncio.wait([t1, t2])
    print(f"{len(done)=}, {len(pending)=}")
    for item in done:
        print(item.result())
    



if __name__ == "__main__":
    asyncio.run(main())