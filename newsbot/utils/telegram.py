import peewee
import re
import requests

from pathlib import Path
from time import sleep
from typing import Dict

from newsbot import log
from .models import db, Source
from .reddit import Reddit
from .states import States


class Telegram:

    def __init__(self, config, states: States) -> None:
        self._config = config
        self._reddit = Reddit(self._config)
        self._states = states
        self._last_updated_path = Path(self._config.last_updated_folder)
        self._api_base = f'https://api.telegram.org/bot{self._config.nbt_access_token}'
        self._err_no_source = 'No sources defined! Set a source using /source list, of, sub, reddits.'
        self._false_response = {"ok": False}
        self._skip_list = []
        self._sources_dict = {}

    def get_updates(self, last_updated: int) -> Dict:
        log.info(f'Checking for requests, last updated passed is: {last_updated}')
        sleep(self._config.update_period)
        response = requests.get(f"{self._api_base}/getUpdates", params={'offset': last_updated+1})
        json_response = self._false_response
        if response.status_code != 200:
            sleep(self._config.update_period*20)
            self.get_updates(last_updated)
        try:
            json_response = response.json()
        except ValueError:
            sleep(self._config.update_period*20)
            self.get_updates(last_updated)
        log.info(f"received response: {json_response}")
        return json_response
    
    def post_message(self, chat_id: str, text: str) -> requests.Response:
        log.debug(f"posting {text} to {chat_id}")
        payload = {'chat_id': chat_id, 'text': text}
        requests.post(f"{self._api_base}/sendMessage", data=payload)

    def handle_incoming_messages(self, last_updated: int) -> None:
        r = self.get_updates(last_updated)
        split_chat_text = []
        if r['ok']:
            for req in r['result']:
                if 'message' in req:
                    chat_sender_id = req['message']['chat']['id']
                else:
                    chat_sender_id = req['edited_message']['chat']['id']
                try:
                    chat_text = req['message']['text']
                    split_chat_text = chat_text.split()
                except KeyError:
                    chat_text = ''
                    split_chat_text.append(chat_text)
                    log.debug('Looks like no chat text was detected... moving on')

                if 'message' in req:
                    person_id = req['message']['from']['id']
                else:
                    person_id = req['edited_message']['from']['id']

                log.info(f"Chat text received: {chat_text}")
                r = re.search('(source+)(.*)', chat_text)

                if (r is not None and r.group(1) == 'source'):
                    if r.group(2):
                        self._sources_dict[person_id] = r.group(2)
                        log.info(f'Sources set for {person_id} to {self._sources_dict[person_id]}')
                        with db.atomic() as txn:
                            try:
                                sources = Source.create(person_id=person_id, fetch_from=self._sources_dict[person_id])
                                log.debug(f'Inserted row id: {sources.person_id}')
                            except peewee.IntegrityError:
                                sources = Source.update(fetch_from=self._sources_dict[person_id]).where(person_id == person_id)
                                rows_updated = sources.execute()
                                log.info(f'Updated {rows_updated} rows')
                            txn.commit()
                        self.post_message(person_id, 'Sources set as {0}!'.format(r.group(2)))
                    else:
                        self.post_message(person_id, 'We need a comma separated list of subreddits! No subreddit, no news :-(')

                if chat_text == '/stop':
                    log.debug(f"Added {chat_sender_id} to skip list")
                    self._skip_list.append(chat_sender_id)
                    self.post_message(chat_sender_id, "Ok, we won't send you any more messages.")

                if chat_text in ('/start', '/help'):
                    helptext = '''
                        Hi! This is a News Bot which fetches news from subreddits. Use "/source" to select a subreddit source.
                        \nExample "/source statistics, python" fetches news from r/statistics, r/python.
                        \nUse "/fetch" for the bot to go ahead and fetch the news. At the moment, bot will fetch total of 5 posts from all sub reddits.
                    '''
                    self.post_message(chat_sender_id, helptext)

                if split_chat_text[0] == '/fetch' and (person_id not in self._skip_list):
                    self.post_message(person_id, 'Hang on, fetching your news...')
                    try:
                        sub_reddits = Source.get(person_id = person_id).fetch_from.strip()
                        summarized_news = self._reddit.get_latest_news(sub_reddits)
                        self.post_message(person_id, summarized_news)
                    except peewee.DoesNotExist:
                        self.post_message(person_id, self._err_no_source)
                
                last_updated = req['update_id']
                self.write_last_updated(last_updated)

    def write_last_updated(self, last_updated: int) -> None:
        filename = self._last_updated_path / 'last_updated.txt'
        with open(filename, 'w') as f:
            f.write(str(last_updated))
            self._states.last_updated_id = last_updated
            log.debug(f'Updated last_updated to {last_updated}')
        f.close()
