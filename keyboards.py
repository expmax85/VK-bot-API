import json


class KeyBoard:

    def get_keyboard(self, btn_list: list, line_len: int = 3):
        keyboard = {
            "one_time": False,
            "buttons": []
        }
        temp = []
        for item in btn_list:
            if (btn_list.index(item) + 1) % line_len == 0:
                keyboard['buttons'].append(temp)
                temp = []
            temp.append(self.get_button(label=str(item)))
        else:
            keyboard['buttons'].append(temp)
        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        return keyboard

    def get_button(self, label, color: str = 'primary'):
        return {
            "action": {
                "type": "text",
                "label": label.capitalize()
            },
            "color": color
        }

    def get_main_kb(self, board_name: str):
        with open(f'keyboards/{board_name}.json', mode='r', encoding='utf-8') as kb:
            return kb.read()


keyboard = KeyBoard()
