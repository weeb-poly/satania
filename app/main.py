import os
import asyncio
from typing import List

import aiohttp
import arrow
from arrow import Arrow
from discord import Embed, Webhook, AsyncWebhookAdapter

from .gcal.parse import get_cal, get_notify_embeds
from .utils import divide_chunks, sleep_till


WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PING_ROLE = os.environ.get('PING_ROLE')


async def send_embeds(embs: List[Embed]) -> None:
    # We only ping when enabled
    send_args = {}
    if PING_ROLE:
        send_args['content'] = f"<@&{PING_ROLE}>"

    # You can only send 10 embeds (events) per request
    # So we separate our requests into chunks of 10
    embs_chunks = divide_chunks(embs, 10)

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(
            WEBHOOK_URL,
            adapter=AsyncWebhookAdapter(session)
        )

        for embs in embs_chunks:
            await webhook.send(**send_args, embeds=embs)


async def schedule_embed(time: Arrow, embed: Embed) -> None:
    await sleep_till(time)
    await send_embeds([embed])


async def schedule_timed_embeds(cal, start: Arrow, end: Arrow) -> None:
    embs = get_notify_embeds(cal, start, end)

    await asyncio.gather(*[
        asyncio.create_task(schedule_embed(time, emb)) for (time, emb) in embs
    ])


async def main() -> None:
    cal = get_cal()
    start = arrow.now().floor('minute')
    end = start.shift(minutes=30)
    await schedule_timed_embeds(cal, start, end)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
