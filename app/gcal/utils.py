import os
import datetime
import pickle

import arrow
from discord import Embed

from googleapiclient.discovery import build
from google.oauth2 import service_account

from ..utils import quickembed


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


def check_valid_creds(token_path: str = "token.pickle") -> bool:
    valid = False

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            credentials = pickle.load(token)
            valid = (credentials and credentials.valid)

    return valid


def gen_service_token(token_path: str = "token.pickle", acct_fn: str = "secret/creds.json") -> None:
    creds = service_account.Credentials.from_service_account_file(
        acct_fn,
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # Need to do something to validate creds
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=2,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    assert creds.valid

    with open(token_path, 'wb') as token:
        pickle.dump(creds, token)
