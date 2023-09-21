from pathlib import Path

from utils.states import States, log
from utils.telegram import Telegram
from config.config import AppConfiguration


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
    config = AppConfiguration()
    update = LastUpdate(config)
    try:
        log.info("Starting up")
        States.last_updated = update.get_last_updated()
        telegram = Telegram(config)
        while True:
            telegram.handle_incoming_messages(States.last_updated)
    except KeyboardInterrupt:
        log.info("Received KeybInterrupt, exiting")


if __name__ == '__main__':
    main()
        