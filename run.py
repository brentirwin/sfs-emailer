import sys
import argparse

from src import *
from src.enums import Frequency
from src.emailer import email

parser = argparse.ArgumentParser()
parser.add_argument("frequency", help="'daily' or 'weekly'", type=str)
args = parser.parse_args()
if args.frequency != 'daily' and args.frequency != 'weekly':
  sys.exit('format: python emailer.py <daily/weekly>')

freq = None
if args.frequency == 'daily':
  freq = Frequency.DAILY
else:
  freq = Frequency.WEEKLY

email(freq)
