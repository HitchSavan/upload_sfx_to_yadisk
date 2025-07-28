import os
import json
import sys
from datetime import date

import yadisk


def create_dir(y, path):
    if not y.exists(path):
        y.mkdir(path)


def upload_file(y, src_path, target_path):
    try:
        y.upload(src_path, target_path)
    except yadisk.exceptions.PathExistsError:
        print(f'{target_path.split("/")[-1]} already exists, updating...')
        y.remove(target_path)
        y.upload(src_path, target_path)


def upload_to_disk(_settings, source_path='', target_path='', _ignored=[]):
    y = yadisk.YaDisk(token=_settings['token'])
    if y.check_token():
        print('Token is correct, uploading')
    else:
        print("Token is incorrect, can't upload")
        sys.exit(3)

    if not target_path:
        target_path = _settings['default_folder']

    td = date.today().strftime("%Y_%m_%d")

    total_path = '/'
    for folder in target_path.split('/'):
        if folder:
            total_path += folder
            create_dir(y, total_path)
            total_path += '/'

    if not source_path:
        total_path += td
        create_dir(y, total_path)
        for file in os.listdir():
            if file.endswith('.exe'):
                executable_name = file
                print(f'Uploading {executable_name}')
                upload_file(y, executable_name,
                            f"{total_path}/{executable_name}")
                print('Upload complete')
                if os.path.exists('old'):
                    if not os.path.exists(os.path.join('old', td)):
                        os.mkdir(os.path.join('old', td))
                else:
                    os.mkdir(os.path.join('old'))
                    os.mkdir(os.path.join('old', td))
                os.replace(os.path.join(executable_name),
                           os.path.join('old', td, executable_name))

    else:
        if os.path.isdir(source_path):
            for adress, dirs, files in os.walk(source_path):
                cur_path = os.path.join(total_path,
                                        adress.replace(source_path, '')[
                                            1:].replace('\\', '/'),
                                        ('/' if adress.replace(source_path, '')[1:] else ''))
                inters = set(_ignored).intersection(cur_path.split('/'))
                if inters:
                    continue
                for subdir in dirs:
                    if subdir in _ignored:
                        continue
                    print(f'Creating dir {subdir} in {cur_path}')
                    create_dir(y, f'{cur_path}{subdir}')
                for file in files:
                    if file in _ignored:
                        continue
                    print(f'Uploading {file} to {cur_path}')
                    upload_file(y, os.path.join(adress, file),
                                f'{cur_path}{file}')
        else:
            source_path = source_path.replace('\\', '/')
            file = source_path.split("/")[-1]
            print(f'Uploading {file} to {total_path}')
            upload_file(y, source_path, f'{total_path}{file}')


if __name__ == '__main__':
    with open('settings.json', encoding='utf-8') as json_file:
        settings = json.load(json_file)

    try:
        source_folder_path = sys.argv[1]
        target_folder_path = sys.argv[2]
    except IndexError:
        print('Not Enough Arguments:')
        print('''\tusage: upload_to_yandex_disk.py
              <source folder or path to file to upload>
              <yandex disk destination folder>''')
        sys.exit(2)

    ignored = ['.git', '.gitignore', '.env',
               'old', '__pycache__', 'config.txt']

    upload_to_disk(settings, source_folder_path,
                   target_folder_path.replace('\\', '/'), ignored)

    print('Complete')
