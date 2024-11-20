import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configure Google Sheets authentication
def setup_google_sheets():
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    json_keyfile = 'student-score-442208-667e5414488a.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    return gspread.authorize(creds)

# Fetch data from Google Sheets
def get_sheet_data(client):
    try:
        spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1sx8K1aGjC9uFQHgAz7t11a3QC3Z7Smlk-IBYJ9qWwoM/edit'
        spreadsheet = client.open_by_url(spreadsheet_url)
        worksheet = spreadsheet.worksheet('SHEET5602105I20241')

        # Fetch all data
        data = worksheet.get_all_records()
        return data

    except Exception as e:
        print(f"Error reading Google Sheet: {str(e)}")
        return None

# Main function
def main():
    client = setup_google_sheets()
    data = get_sheet_data(client)

    if data:
        print("Google Sheet Data:")
        # Print all records
        for record in data:
            print(record)

if __name__ == "__main__":
    main()
