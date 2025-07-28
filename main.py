import json
import sys
import os

from create_sfx import create_sfx
from upload_to_yandex_disk import upload_to_disk

if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(sys.argv[0]), 'settings.json'),
              encoding='utf-8') as json_file:
        settings = json.load(json_file)
    try:
        source_folder_path = sys.argv[1]
    except IndexError:
        print('Not Enough Arguments:')
        print('\tusage: main.py <input build folder>')
        sys.exit(2)

    create_sfx(settings, source_folder_path)

    upload_to_disk(settings)
