from dotenv import load_dotenv
from sys import exit
import os

load_dotenv()

ERR_NO_SOURCE = 'No sources defined! Set a source using /source list, of, sub, reddits'
skip_list = []
sources_dict = {}
UPDATE_PERIOD = 1
FALSE_RESPONSE = {"ok": False}

BOT_KEY = os.getenv('NBT_ACCESS_TOKEN')
if not BOT_KEY:
    print("Telegram access token not set, exiting.")
    exit(1)
API_BASE = f'https://api.telegram.org/bot{BOT_KEY}'
