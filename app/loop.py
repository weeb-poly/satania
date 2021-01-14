import asyncio

import arrow
import uvloop

from .once import schedule_timed_embeds
from .utils import sleep_till

from .gcal.parse import get_cal


async def main() -> None:
    # cal = get_cal()
    cal = None
    start = arrow.now().floor('minute')
    end = start.clone()

    while True:
        # Attempt to avoid issues with auth
        # by forcefully reloading the calendar
        # every iteration of the loop
        cal = get_cal()
        start = end
        end = end.shift(minutes=20)
        await schedule_timed_embeds(cal, start, end)
        await sleep_till(end)


def cli() -> None:
    uvloop.install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    cli()
