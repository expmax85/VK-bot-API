import logging
import os
import time
import traceback

import vk_api.vk_api
import requests
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll

from config import UPLOAD_URL
from database import Database
from bot.handlers import Handler
from bot.keyboards import KeyBoard

logging.basicConfig(filename='logs/debug.log',
                    filemode='a',
                    format='%(levelname)s: %(asctime)s - %(message)s',
                    level=logging.INFO)


class VkBot:

    def __init__(self, token: str, group_id: int, database: 'Database', timeout: int = 5) -> None:
        self.vk = vk_api.VkApi(token=token)
        self.long_poll = VkBotLongPoll(vk=self.vk, group_id=group_id)
        self.vk_api = self.vk.get_api()
        self.kb = KeyBoard()
        self.db = database
        self.handler = Handler()
        self.timeout = timeout

    def start(self) -> None:
        logging.info('Run main cycle...')
        try:
            for event in self.long_poll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    msg = event.obj['message']['text'].lower()
                    from_id = event.obj['message']['from_id']
                    buttons = self.db.get_categories()
                    if msg in ['our goods', 'back to categories']:
                        self.send_msg(peer_id=from_id, msg=self.handler.msg_handler(msg),
                                      kb=self.kb.get_keyboard(btn_list=buttons))
                    elif msg in [str(item).lower() for item in buttons]:
                        goods = self.db.get_goods_by_cty(msg)
                        for good in goods:
                            try:
                                img = self.get_img(str(good.image))
                            except FileNotFoundError:
                                img = None
                            self.send_msg(peer_id=from_id, msg=str(good), img=img,
                                          kb=self.kb.get_kb_from_json('back'))
                    else:
                        self.send_msg(peer_id=from_id, msg=self.handler.msg_handler(msg),
                                      kb=self.kb.get_kb_from_json('main'))
        except Exception:
            err = traceback.format_exc()
            logging.error(f'error: {err}')
            logging.info('Error running bot. Reloading...')
            time.sleep(self.timeout)

    def send_msg(self, peer_id: str, msg: str, kb: str = None, img: str = None) -> None:
        self.vk.method('messages.send', {"peer_id": peer_id, "message": msg, "keyboard": kb,
                                         "attachment": img, "random_id": 0})

    def get_img(self, path: str) -> str:
        server_img = self.vk.method("photos.getMessagesUploadServer")
        response = requests.post(server_img['upload_url'], files={'photo': open(os.path.join(UPLOAD_URL, path),
                                                                                'rb')}).json()
        save_img = self.vk.method('photos.saveMessagesPhoto', {'photo': response['photo'],
                                                               'server': response['server'],
                                                               'hash': response['hash']})[0]
        img = "photo{}_{}".format(save_img["owner_id"], save_img["id"])
        return img
