import json
import copy
import threading
from datetime import datetime
import config

class Thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def reload_config():
    tmp = copy.deepcopy(config.config)
    with open('config.json') as json_file:
        config.config = json.load(json_file)
        config.config['TMP'] = tmp['TMP']
    return config.config

def write_config():
    tmp_config = copy.deepcopy(config.config)
    tmp_config.pop('TMP', None)
    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(tmp_config, f, ensure_ascii=False, indent=2)


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
