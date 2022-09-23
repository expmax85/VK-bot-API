
class Handler:
    command = {
        'Привет': 'Здравствуйте. Я тестовый чат-бот пекарни. Чем могу помочь?',
        'help': 'Здесь когда-нибудь будет справка о том, как со мной общаться.',
        'our goods': 'Выберите категорию:',
        'back to categories': 'Выберите категорию:',
    }
    error_msg = 'Я вас не понимаю. Выберите команду или обратитесь в моим создателям.'

    def msg_handler(self, msg: str) -> str:
        if self.command.get(msg):
            return self.command[msg]
        else:
            return self.error_msg
