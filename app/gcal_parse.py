import os

from arrow import Arrow
from gcsa.google_calendar import GoogleCalendar

from .gcal_utils import event2embed


GCAL_ID = os.environ.get('GCAL_ID')


async def get_cal():
    return GoogleCalendar(GCAL_ID, token_path="./token.pickle")


async def get_embeds(cal, start: Arrow, end: Arrow):
    events = []

    events_res = cal.get_events(
        time_min=start.datetime,
        time_max=end.datetime,
        order_by="startTime"
    )

    # TODO: Use event.reminders to schedule notifications

    for event in events_res:
        events.append(event2embed(event))
    
    return events


async def get_notify_embeds(cal, start: Arrow, end: Arrow):
    events = []

    events_res = cal.get_events(
        time_min=start.datetime,
        time_max=end.datetime,
        order_by="startTime"
    )

    # TODO: Use event.reminders to schedule notifications

    for event in events_res:
        embed = event2embed(event)
        for reminder in event.reminders:
            if isinstance(reminder, PopupReminder):
                pingTime = arrow.get(event.start).shift(minutes=-1*minutes_before_start)
                if pingTime >= start:
                    events.append((pingTime, embed,))

    return events
