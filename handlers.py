
class Handler:
    def __init__(self, user_id: str = None, peer_id: str = None, msg: str = None):
        self.user_id = user_id
        self.peer_id = peer_id
        self.msg = msg

    def msg_handler(self, msg: str):
        if msg == '1':
            return 'help'
        elif msg in ['our goods', 'back to categories']:
            return 'Choose category'
        else:
            return 'Я Вас не понимаю. Выберите категорию:'
