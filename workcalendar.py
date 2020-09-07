from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_dates():
    date_time = input('Enter date and time (DD/MM HH-HH): ')

    if date_time == 'quit':
        start = 'quit'
        end = 'quit'

    else:
        date, time = date_time.split()
        day, month = date.split('/')
        start_time, end_time = time.split('-')
        start = f'2020-{month}-{day}T{start_time}:00:00'
        end = f'2020-{month}-{day}T{end_time}:00:00'

    return start, end


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    finished = False

    while not finished:
        start_details, end_details = get_dates()

        if start_details == 'quit':
            finished = True

        else:
            event = {
                'summary': 'WorkAuto',
                'start': {
                    'dateTime': start_details,
                    'timeZone': 'Europe/Dublin',
                },
                'end': {
                    'dateTime': end_details,
                    'timeZone': 'Europe/Dublin',
                },
                "colorId": '5',
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    main()
