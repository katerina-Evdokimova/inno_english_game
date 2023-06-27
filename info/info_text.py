import json
import os

try:
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'text.json')
    with open(filename, "r", encoding='utf8') as read:
        text_info = json.load(read)
except FileNotFoundError as e:
    command = 'error'
    print(e)