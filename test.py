from googleapiclient.discovery import build
from oauth2client import file, client
credentials = client.AccessTokenCredentials('ACCESS_TOKEN', 'USER_AGENT')
service = build('calendar', 'v3', credentials=credentials)
calendars = service.calendarList().list().execute()