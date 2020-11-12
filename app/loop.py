import asyncio

import arrow
import uvloop

from .main import schedule_timed_embeds
from .utils import sleep_till

from .gcal.parse import get_cal


async def main() -> None:
    cal = get_cal()
    start = arrow.now().floor('minute')
    end = start.clone()

    while True:
        start = end
        end = end.shift(minutes=20)
        await schedule_timed_embeds(cal, start, end)
        await sleep_till(end)


if __name__ == '__main__':
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
