import os
from pathlib import Path
from time import sleep

import pymysql
from peewee import OperationalError

from utils.models import db, Source, Request, Message
from utils.states import States
from utils.telegram import Telegram
from config.config import AppConfiguration
from newsbot import log


class LastUpdate:

    def __init__(self, config) -> None:
        self._config = config
        self._last_updated_path = Path(self._config.last_updated_folder)

    def get_last_updated(self) -> int:
        filename = self._last_updated_path / 'last_updated.txt'
        try:
            with open(filename, 'r') as f:
                try:
                    last_updated = int(f.read())
                except ValueError:
                    last_updated = 0
            f.close()
        except FileNotFoundError:
            last_updated = 0
        log.debug(f"Last updated id: {last_updated}")
        return last_updated


def main():
    log.info('Starting up')
    log.info('Waiting 60 seconds for db to come up')
    sleep(60)

    log.info('Checking on dbs')
    try:
        db.connect()
    except OperationalError as e:
        error_code, message = e.args[0], e.args[1]
        if error_code == 1049:
            db_connection = pymysql.connect(host='mysql', user= 'root', password='dontusethisinprod')
            db_connection.cursor().execute('CREATE DATABASE newsbot')
            db_connection.close()
        db.create_tables([Source, Request, Message], True)

    try:
        config = AppConfiguration()
    except Exception as e:
        print(f'ERROR: An error occurred while loading configuration. It is missing an environment variable.\n', flush=True)
        raise EnvironmentError('Environment variables are missing')

    if 'NBT_ACCESS_TOKEN' in os.environ:
        print(f'Using NBT_ACCESS_TOKEN: {os.environ["NBT_ACCESS_TOKEN"]}\n', flush=True)
    else:
        print('WARNING: Using the default value for NBT_ACCESS_TOKEN\n', flush=True)

    update = LastUpdate(config)
    states = States()
    try:
        log.info("Starting newsbot")
        states.last_updated_id = update.get_last_updated()
        telegram = Telegram(config, states)
        while True:
            telegram.handle_incoming_messages(states.last_updated_id)
    except KeyboardInterrupt:
        log.info("Received KeybInterrupt, exiting")


if __name__ == '__main__':
    main()
        