from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetClient:
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        self.creds = Credentials.from_service_account_file("service-account.json", scopes=SCOPES)

    def read_values(self, sheet_name, range):
        read_range = f"{sheet_name}!{range}"
        service = build('sheets', 'v4', credentials=self.creds)
        result = service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                        range=read_range).execute()
        values = result.get('values', [])
        if not values:
            return None
        else:
            return values
    def update_values(self, sheet_name, range, values):
        try:
            write_range = f"{sheet_name}!{range}"
            service = build('sheets', 'v4', credentials=self.creds)
            body = {'values' : values, 'majorDimension': 'ROWS'}
            result = service.spreadsheets().values().update(spreadsheetId=self.spreadsheet_id, range=write_range, valueInputOption='RAW', body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
        except HttpError as error:
            print(f"An error occurred: {error}")

    def clear_values_in_range(self, sheet_name, range):
        try:
            service = build('sheets', 'v4', credentials=self.creds)
            range = f"{sheet_name}!{range}"
            result = service.spreadsheets().values().clear(spreadsheetId=self.spreadsheet_id,
                                            range=range).execute()
            print(f"Succesfully cleared range: {result.get('clearedRange')}")
        except HttpError as error:
            print(f"An error occurred: {error}")
