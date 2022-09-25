from typing import Dict
import json


class KeyBoard:

    def get_keyboard(self, btn_list: list, line_len: int = 3) -> str:
        key_board = {
            "one_time": False,
            "buttons": []
        }
        temp = []
        for item in btn_list:
            if (btn_list.index(item) + 1) % line_len == 0:
                key_board['buttons'].append(temp)
                temp = []
            temp.append(self._get_button(label=str(item)))
        else:
            key_board['buttons'].append(temp)
        key_board = json.dumps(key_board, ensure_ascii=False).encode('utf-8')
        return str(key_board.decode('utf-8'))

    def _get_button(self, label: str, color: str = 'primary') -> Dict:
        return {
            "action": {
                "type": "text",
                "label": label.capitalize()
            },
            "color": color
        }

    def get_kb_from_json(self, board_name: str):
        with open(f'keyboards/{board_name}.json', mode='r', encoding='utf-8') as kb:
            return kb.read()
