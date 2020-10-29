import os
import asyncio
from typing import List

import aiohttp
import arrow
from arrow import Arrow
from discord import Embed, Webhook, AsyncWebhookAdapter

from .gcal_parse import get_cal, get_embeds
from .utils import divide_chunks, sleep_till


WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PING_ROLE = os.environ.get('PING_ROLE')


async def send_embeds(embs: List[Embed]) -> None:
    # We only ping when enabled
    send_args = {}
    if PING_ROLE is not None:
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


async def schedule_embed(time: Arrow, embed: Embed):
    await sleep_till(time)
    await send_embeds([embed])


async def update_channel(start: Arrow, end: Arrow) -> None:
    cal = await get_cal()
    embs = await get_embeds(cal, start, end)
    await send_embeds(embs)


async def schedule_channel_notifications(start: Arrow, end: Arrow) -> None:
    cal = await get_cal()
    embs = await get_notify_embeds(cal, start, end)
    for (time, emb) in embs:
        asyncio.create_task(schedule_embed(time, emb))


async def main():
    start = arrow.now()
    end = start.shift(minutes=30)
    await update_channel(start, end)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
