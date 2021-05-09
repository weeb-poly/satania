import os
from typing import List, Tuple, Iterator

import arrow
from arrow import Arrow
from discord import Embed
from gcsa.google_calendar import GoogleCalendar

from .utils import event2embed, check_valid_creds, gen_service_token


GCAL_ID = os.environ.get('GCAL_ID')
GAPP_CREDS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', './secret/creds.json')
GAPP_TOK = os.environ.get('GOOGLE_APPLICATION_TOKEN', './token.pickle')


def get_cal() -> GoogleCalendar:
    # Since we're using a serivce account
    # and gcsa doesn't support service accounts
    # I made a workaround

    if not check_valid_creds(GAPP_TOK):
        gen_service_token(GAPP_TOK, GAPP_CREDS)

    return GoogleCalendar(
        calendar=GCAL_ID,
        read_only=True,
        token_path=GAPP_TOK
    )


def get_embeds(cal: GoogleCalendar, start: Arrow, end: Arrow) -> List[Embed]:
    events_res = cal.get_events(
        time_min=start.datetime,
        time_max=end.datetime,
        order_by="startTime"
    )

    events = list(map(lambda e: event2embed(event), events_res))

    return events


def get_notify_embeds(cal: GoogleCalendar, start: Arrow, end: Arrow) -> List[Tuple[Arrow, Embed]]:
    events_res = cal.get_events(
        time_min=start.datetime,
        time_max=end.datetime,
        order_by="startTime"
    )

    embeds = []

    for event in events_res:
        embed = event2embed(event)

        if len(event.reminders) == 0:
            # One Notification at the time of the event
            pingTime = arrow.get(event.start)
            # if pingTime.is_between(start, end, '[)'):
            #     yield (pingTime, embed,)

            # One notification 10 mins before
            pingTime = pingTime.shift(minutes=-10)
            if pingTime.is_between(start, end, '[)'):
                embeds.append((pingTime, embed,))

        # There's currently a bug in gcsa
        # event.reminders is always empty
        # so this never gets triggered
        for r in event.reminders:
            if isinstance(r, PopupReminder):
                min_shift = -1*r.minutes_before_start
                pingTime = arrow.get(event.start).shift(minutes=min_shift)
                if pingTime.is_between(start, end, '[)'):
                    embeds.append((pingTime, embed,))

    return embeds
