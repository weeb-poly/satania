import asyncio

import arrow

from .main import update_channel


async def main():
    start = None
    end = arrow.now()
    while True:
        start = end.clone()
        end = end.shift(minutes=20)
        await update_channel(start, end)
        sleep_time = (end - arrow.now()).total_seconds()
        await asyncio.sleep(sleep_time)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
