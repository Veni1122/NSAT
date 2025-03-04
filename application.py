import os

import logging

from app_config import AppConfig

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__file__)


class Application:

    def __init__(self):
        from frames.main_window import MainFrame

        os.environ["DISPLAY"] = ":0"

        local_dev_mode = bool(os.getenv("LOCAL_DEV"))
        if local_dev_mode:
            logger.info(f'Local dev mode activated')

        # Init Configuration
        AppConfig()

        # Init user interface
        self.main_window = MainFrame(local_dev_mode)


if __name__ == '__main__':
    # Start App
    Application()
