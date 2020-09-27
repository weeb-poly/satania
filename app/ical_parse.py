import os

import arrow
import aiohttp
from ics import Calendar

from .ical_utils import timeline_patch, event2embed, rrule

ICAL_URL = os.environ.get('ICAL_URL')


async def get_cal():
    async with aiohttp.ClientSession() as session:
        async with session.get(ICAL_URL) as resp:
            return Calendar(await resp.text())
    return None


async def get_embeds(c, start, end):
    t = timeline_patch(c.timeline)

    events = {}
    event_rrule = {}

    for e in t.start_included(start, end):
        if e.uid not in events:
            events[e.uid] = event2embed(e)
            event_rrule[e.uid] = rrule(e)
        else:
            if event_rrule[e.uid] is not None:
                events[e.uid] = event2embed(e)
            event_rrule[e.uid] = rrule(e)
    
    return list(events.values())
