import asyncio


async def abc():
    while True:
        await asyncio.sleep(0)
        print(123)


if __name__ == '__main__':
    try:
        asyncio.run(abc())
    except KeyboardInterrupt as e:
        print(e)
    print(22)
