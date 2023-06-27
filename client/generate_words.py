import random

KEY = "khxRU+NZabVM0QHOYC3uxw==7374zGaMtsryRVHC"
import requests
import json
import os



def generate_words(letter):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'result.json')
        with open(filename, "r", encoding='utf8') as read:
            dic = json.load(read)
        return random.choices(dic[letter])[0]
    except FileNotFoundError as e:
        # command = 'error'
        print(e)
