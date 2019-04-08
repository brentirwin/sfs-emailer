import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .config import gdrive_config

def addresses():

  # API Client
  scope = ['https://www.googleapis.com/auth/spreadsheets']
  creds = ServiceAccountCredentials.from_json_keyfile_name(
          'src/client_secret.json', scope)
  client = gspread.authorize(creds)

  # Addresses
  sheet = client.open_by_key(
          gdrive_config['addresses']).worksheet(
          'Addresses')

  # Remove dots
  addr_list = []
  for i in sheet.col_values(1):
    address = i
    if 'gmail' in i:
      split_addr = i.split('@')
      split_addr[0] = split_addr[0].replace('.', '')
      address = '@'.join(split_addr)
    addr_list.append(address)

  return ', '.join(addr_list)
