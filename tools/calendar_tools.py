import datetime
import os.path
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

TOOLS_DIR=Path(__file__).resolve().parent
SCHEDULEME_DIR=TOOLS_DIR.parent
CREDENTIALS_PATH=str(SCHEDULEME_DIR / 'credentials.json')
TOKEN_PATH=str(SCHEDULEME_DIR / 'token.json')


# If modifying these scopes, delete the file token.json.
# 'calendar' gives read/write access. 'calendar.readonly' gives read-only access.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    # Build and return the API client service
    return build('calendar', 'v3', credentials=creds)

def get_upcoming_events(service, max_results=5):
    print(f"\n--- Fetching the next {max_results} upcoming events ---")
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    
    events_result = service.events().list(
        calendarId='primary', 
        timeMin=now,
        maxResults=max_results, 
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return
    return events

def create_event(service, summary, description, start_time_iso, end_time_iso):
    print(f"\n--- Creating event: '{summary}' ---")
    event_body = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time_iso, # e.g., '2026-05-25T10:00:00+03:00'
            'timeZone': 'Asia/Qatar',
        },
        'end': {
            'dateTime': end_time_iso,
            'timeZone': 'Asia/Qatar',
        },
    }

    created_event = service.events().insert(calendarId='primary', body=event_body).execute()
    return created_event.get('htmlLink')

def availability_check(service,start_time,end_time):

    event_result= service.events().list(
        calendarId="primary",
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events=event_result.get('items',[])
    
    if len(events)==0:
        return "No Events Found. You are available!"
    else:
        return events
    
def modify_event(service,event_id,summary=None,description=None,start_time_iso=None,end_time_iso=None):
    event = service.events().get(
        calendarId='primary', 
        eventId=event_id
        ).execute()


    if summary:
        event['summary'] = summary
    if description:
        event['description'] = description
    if start_time_iso:
        event['start'] = {
            'dateTime': start_time_iso,
            'timeZone': 'Asia/Qatar',
        }
    if end_time_iso:
        event['end'] = {
            'dateTime': end_time_iso,
            'timeZone': 'Asia/Qatar',
        }

    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return updated_event.get('htmlLink')

from googleapiclient.errors import HttpError


def remove_event(service, event_id):

    try:

        service.events().delete(
            calendarId="primary",
            eventId=event_id
        ).execute()

        return {
            "success": True,
            "message": "Event deleted successfully."
        }

    except HttpError as e:

        return {
            "success": False,
            "message": str(e)
        }


if __name__ == '__main__':
    # 1. Initialize the service
    calendar_service = get_calendar_service()
    
    # 2. Fetch and print upcoming events
    events = get_upcoming_events(calendar_service, max_results=5)

    event=events[0]

    print("Event",event["summary"],event["id"])
    delete_event=remove_event(calendar_service,event["id"])
    print(delete_event)
    #new_event=modify_event(calendar_service,event['id'],summary=new_summary)
    #print(f"Event updated: {new_event}")