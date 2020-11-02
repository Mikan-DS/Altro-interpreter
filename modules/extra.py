import json


def create_button(text, num):
    """Cоздает кнопку"""
    return {
        "action": {
            "type": "text",
            "payload": "{\"choice\":\"" + num + "\"}",
            "label": f"{'/' + str(int(num) + 1) + ' - ' + text}"
        },
    }


def create_keyboard(buttons):
    """Создает клавиатуру"""
    keyboard = {
        "inline": True,
        "buttons": [[create_button(j[0], str(i))] for i, j in enumerate(buttons)]
    }

    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


PYTHON = lambda code, player: eval(code, {"player": player})
