import logging
import time
import traceback

import vk_api.vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from databases import db
from handlers import Handler
from keyboards import keyboard

logging.basicConfig(filename='logs/log.log',
                    filemode='a',
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    level=logging.INFO)


class VkBot:

    def __init__(self, token: str, group_id: int) -> None:
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(vk=self.vk, group_id=group_id)
        self.vk_api = self.vk.get_api()
        self.db = db
        self.main_kb = keyboard.get_main_kb('main')
        self.handler = Handler()

    def start(self):
        logging.info('Запуск основного цикла...')
        try:
            for event in self.long_poll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    msg = event.obj['message']['text'].lower()
                    from_id = event.obj['message']['from_id']
                    buttons = self.db.get_categories()
                    if msg in ['our goods', 'back to categories']:
                        self.send_msg(peer_id=from_id, msg=self.handler.msg_handler(msg),
                                      keyboard=keyboard.get_keyboard(btn_list=buttons))
                    elif msg in [str(item).lower() for item in buttons]:
                        goods = db.get_goods_by_cty(msg)
                        for good in goods:
                            self.send_msg(peer_id=from_id, msg=str(good),
                                          keyboard=keyboard.get_main_kb('back'))
                    else:
                        self.send_msg(peer_id=from_id, msg=self.handler.msg_handler(msg),
                                      keyboard=self.main_kb)
        except Exception:
            err = traceback.format_exc()
            print('Ошибка при запуске бота')
            logging.error(f'error: {err}')
            logging.info('Reloading...')
            time.sleep(5)

    def send_msg(self, peer_id, msg, keyboard=None):
        self.vk.method('messages.send', {"peer_id": peer_id, "message": msg, "keyboard": keyboard, "random_id": 0})
