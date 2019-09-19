import asyncio
from time import sleep

loop = asyncio.get_event_loop()

async def hello():
    print('Hello ...')
    await asyncio.sleep(3)
    print('World!')
    print()


def hello_old():
    print('Hello ........')
    sleep(3)
    print('World!')


async def main():
    await asyncio.wait( [
        #hello_old(), hello_old(), hello_old(), hello_old(), hello()
        hello(), hello(), hello(), hello(), hello()
        ])

if __name__ == '__main__':    

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
