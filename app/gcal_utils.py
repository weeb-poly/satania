import datetime
import pickle

import arrow
from discord import Embed

from googleapiclient.discovery import build
from google.oauth2 import service_account

from .utils import quickembed


def event2embed(e) -> Embed:
    desc = e.description
    if desc is None:
        desc = "<i>No Info Available</i>"
    return quickembed(
        e.summary,
        desc,
        arrow.get(e.start),
        arrow.get(e.end)
    )


def gen_service_token() -> None:
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    SERVICE_ACCOUNT_FILE = 'service_creds.json'

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # Need to do something to validate creds
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=2, singleEvents=True,
                                        orderBy='startTime').execute()

    with open('token.pickle', 'wb') as token:
        assert creds.valid
        pickle.dump(creds, token)
