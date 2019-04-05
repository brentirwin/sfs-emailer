import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .config import gdrive_config

def addresses():
  '''
  # API Client
  scope = ['https://www.googleapis.com/auth/spreadsheets']
  creds = ServiceAccountCredentials.from_json_keyfile_name(
          'src/client_secret.json', scope)
  client = gspread.authorize(creds)

  # Addresses
  sheet = client.open_by_key(
          gdrive_config['Addresses']).worksheet(
          'Addresses')
  return ', '.join(sheet.col_values(1))
  '''
  return 'me@brentirw.in'
