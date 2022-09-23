import logging
import time

from config import vk_api_token, group_id, test_data
from database.databases import db
from database.models import create_models
from bot.vk_bot import VkBot


if __name__ == '__main__':
    create_models()
    if test_data:
        check_exists = db.get_categories()
        if not check_exists:
            db.insert_test_data()

    logging.info('Loading bot...')
    while True:
        try:
            bot = VkBot(token=vk_api_token, group_id=group_id)
            bot.start()
        except Exception as err:
            logging.error(f'Error: {err}')
            logging.info('Reloading...')
            time.sleep(2)
