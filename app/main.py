import os
import asyncio

import aiohttp
import arrow
from discord import Webhook, AsyncWebhookAdapter

from .ical_parse import get_cal, get_embeds
from .utils import divide_chunks


WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
PING_ROLE = os.environ.get('PING_ROLE')


async def send_embeds(embs):
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


async def update_channel(start, end):
    cal = await get_cal()
    embs = await get_embeds(cal, start, end)
    await send_embeds(embs)


async def main():
    now = arrow.now()
    start = now
    end = start.shift(minutes=20)
    await update_channel(start, end)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
