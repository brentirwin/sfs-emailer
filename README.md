# sfs-emailer

This script pulls data from the SFS ROTA on Google Docs and generates daily and weekly call emails as necessary.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Add these lines to `crontab -e`:
```
5 6 * * * /PATH/TO/SCRIPT/run.py daily
* 6 1 * * /PATH/TO/SCRIPT/run.py weekly
```
to run the daily script every morning at 6:05am and the weekly script every Monday morning at 6am.

Google Drive API info saved at `src/client_secret.json` exactly as it's downloaded.

