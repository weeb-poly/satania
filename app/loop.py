import asyncio

import arrow

from .main import update_channel
from .utils import sleep_till


async def main():
    start = arrow.now()
    end = start.clone()
    while True:
        start = end
        end = end.shift(minutes=20)
        await update_channel(start, end)
        await sleep_till(end)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
