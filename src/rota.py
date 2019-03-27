import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .config import gdrive_config
from .config import rota_config
from .enums import Frequency

from .sample_rota import sample_rota

# Get the ROTA from Google Sheets and return a 2D array
def get_rota():
  # API Client
  scope = ['https://www.googleapis.com/auth/spreadsheets']
  creds = ServiceAccountCredentials.from_json_keyfile_name(
          'client_secret.json', scope)
  client = gspread.authorize(creds)

  # Addresses
  rota_raw = client.open_by_key(
             gdrive_config['rota']).worksheet(
             'ROTA Ver2')
  rota = []
  for row in range(rota_config['rows'][0], rota_config['rows'][1]):
    values = rota_raw.row_values(row)
    rota.append(values[1:18])

  return rota

# Take a formatted date a return a differently-formatted date
# date: String format: '12th April'
def get_date(date):
  date = date + ' 2019'
  date = date.replace('st','')
  date = date.replace('nd','')
  date = date.replace('rd','')
  date = date.replace('th','')
  date = datetime.datetime.strptime(date, '%d %B %Y')
  return date.strftime('%A, %B %d')

# Take the show time and return the showtime properly formatted,
# along with the dates for the rest of the schedule.
# time: type=datetime
def get_times(time):
  def format_time(timestamp):
    return timestamp.strftime('%I:%M %p')

  show_time = time
  time = datetime.datetime.strptime(time, '%I:%M %p')
  schedule = {
    'drink_up_call': format_time(time - datetime.timedelta(hours=4)),
    'ensemble_call': format_time(time - datetime.timedelta(hours=1, minutes=30)),
    'fight_dance_call': format_time(time - datetime.timedelta(hours=1, minutes=15)),
    'mic_check': format_time(time - datetime.timedelta(hours=1)),
    'house_open': format_time(time - datetime.timedelta(minutes=45))
  }
  return show_time, schedule

# show: 1 row of data
# Return a special value if it exists in that column. Otherwise, return a default
def get_optional(show, i, default):
  return show[i] if (i < len(show) and show[i] != '') else default

# Take a row of data and return 1 Dictionary of a show
# show: 1 row of data
def single_show(show):
  time, schedule = get_times(show[2])
  
  return {
    'date': get_date(show[0]),
    'time': time,
    'schedule': schedule,
    'location': get_optional(show, 14, 'Spiderhouse Ballroom'),
    'drink_up': get_optional(show, 17, 'TBA'),
    'cast': {
      'juliet':     show[3],
      'benvolia':   show[4],
      'romeo':      show[5],
      'mercutio':   show[6],
      'tybalt':     show[7],
      'compere':    show[8],
      'board_op':   show[9],
      'showrunner': show[10]
    },
    'roles': {
      'drinker':    show[11],
      'alternate':  show[12],
      'wrangler':   show[12]
    }
  }

# Return a daily call, which is a single show and info for the next show
def daily_call(rota):
  # Get today's date in string form
  now = datetime.datetime.now().strftime('%d %B %Y')

  # Initialize the shows to be None
  show = None
  next_show = None
  
  # Find a show that matches today's date if there is one, otherwise the value will remain None
  # If there is a next show, add that one too
  for row in range(len(rota)):
    if get_date(rota[row][0]) == now:
      show = rota[row]
      if len(rota) > row+1:
        next_show = rota[row+1]
      break
  
  # If there is a show, get the show in Dictionary format
  # If there is a next show, append it
  if show:
    call = single_show(show)
    if next_show:
      call['next_show'] = {
        'date': get_date(next_show[0]),
        'location': get_optional(next_show, 14, 'Spiderhouse Ballroom'),
        'cast': list(dict.fromkeys(next_show[4:11]))
      }
    return [call]
  return None

# Return all shows in the upcoming week, starting now
def weekly_call(rota):
  # Get a timestamp for now and next week
  now = datetime.datetime.now()
  then = now + datetime.timedelta(weeks=1)

  # Open an empty array for the week's shows
  shows = []

  # For each row, convert the date to a datetime
  for row in range(len(rota)):
    date = datetime.datetime.strptime(rota[row][0], '%d %B %Y')
    # If the date is past next week, quit looking
    if date > then:
      break
    # If the date is past today, append it to the list
    if date > now:
      show.append(row)

  # If there are no shows, return None
  if len(shows) == 0:
    return None
  
  # Get single show data for each show in the week and return it as an array
  for show in shows:
    shows[show] = single_show(rota[show])

  return shows

# Takes a frequency and returns a call in Dictionary format based on the current time/date
def get_call(frequency):
# rota = get_rota()
  rota = sample_rota

  if frequency == Frequency.DAILY:
    return daily_call(rota)
  else:
    return weekly_call(rota)
