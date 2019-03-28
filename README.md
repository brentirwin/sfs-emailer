# sfs-emailer

This script pulls data from the SFS ROTA on Google Docs and generates daily and weekly call emails as necessary.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Add these lines to `crontab -e`:
```
5 6 * * * /PATH/TO/SCRIPT/run.py daily -e
* 6 1 * * /PATH/TO/SCRIPT/run.py weekly -e
```
to run the daily script every morning at 6:05am and the weekly script every Monday morning at 6am.

Google Drive API info saved at `src/client_secret.json` exactly as it's downloaded.

Create a file at `src/config.py` with the following format:
```python
email_config = {
  'from': '',
  'password': '',
  'emergency': '' # Emergency contact if emails fail
}

gdrive_config = {
  'addresses': 'GDRIVE_DOCUMENT_ID',
  'rota': 'GDRIVE_DOCUMENT_ID'
}

rota_config = {
  'rows': [7, 23] # Can be updated if shows are added or removed, span of relevant content
}
```
