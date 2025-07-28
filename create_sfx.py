import os
import sys
import json


def create_sfx(_settings, _source_folder_path, _ignored=[]):
    executable_name = ''
    if _settings["use_executable_name"]:
        for file in os.listdir(_source_folder_path):
            if file.endswith('.exe'):
                executable_name = file

    archive_name = os.path.split(_source_folder_path)[-1]

    create_archive_command = f'7z a -t7z {archive_name}.7z -m0=lzma2 -mx=9 -aoa'

    if _settings:
        for item in _settings["include_files"]:
            create_archive_command += f' {_source_folder_path}{item}'
        if "additional_files" in _settings.keys():
            for item in _settings["additional_files"]:
                create_archive_command += f' {_source_folder_path}{item}'
    else:
        create_archive_command += f' {_source_folder_path}\\*'

    if executable_name:
        config = f''';!@Install@!UTF-8!\n
                InstallPath="{executable_name[:-4]}"\n
                RunProgram="{executable_name}"\n
                GUIMode="2"\n
                ;!@InstallEnd@!'''
    else:
        config = f''';!@Install@!UTF-8!\n
                InstallPath="{archive_name}"\n
                GUIMode="2"\n
                ;!@InstallEnd@!'''
        executable_name = f'{archive_name}.exe'

    zip_module = ''
    for file in os.listdir(os.path.dirname(__file__)):
        if file.endswith('.sfx'):
            zip_module = file

    if zip_module == '':
        raise FileNotFoundError('cannot find .sfx modulr file')

    create_sfx_command = f'COPY /b {zip_module} + config.txt + {archive_name}.7z {executable_name}'

    with open('config.txt', 'w', encoding='utf-8') as f:
        f.write(config)

    print(create_archive_command)
    os.system(create_archive_command)
    print('---------------')
    print(create_sfx_command)
    os.system(create_sfx_command)

    os.remove(f'{archive_name}.7z')


if __name__ == '__main__':
    try:
        source_folder_path = sys.argv[1]
    except IndexError:
        print('Not Enough Arguments:')
        print('\tusage: create_sfx.py <input source folder>')
        sys.exit(2)

    with open('settings.json', encoding='utf-8') as json_file:
        settings = json.load(json_file)

    ignored = []

    create_sfx(settings, source_folder_path, ignored)
