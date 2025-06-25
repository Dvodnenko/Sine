import json, os
from pathlib import Path

from .views import ask


DATA_PATH = Path.home() / '.rawdata.json'


# datafile management

def create_datafile():
    os.system(f'touch {DATA_PATH}')

def apply_basic_markup():
    data = {
        'tags': [],
        'active_session': {},
        'sessions': ''
    }

    with open(DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)


# data management

def read_data() -> dict:
    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data
    except FileNotFoundError as _:
        print(f'🦇 error: datafile not found at {DATA_PATH}')
        if ask('do you want to create it (y/n)? ') == True:
            create_datafile()
            apply_basic_markup()

            print(f'🦇 datafile created at {DATA_PATH}')
            print('basic markup applied')
            exit(0)
        else:
            exit(1)

def get_field(data_dict: dict, field: str):
    value = data_dict.get(field)

    return value

def rewrite_data(new_data: dict) -> None:
    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, ensure_ascii=False, indent=4)

        return None
    except FileNotFoundError as _:
        print(f'🦇 error: datafile not found at {DATA_PATH}')
        if ask('do you want to create it (y/n)? ') == True:
            create_datafile()
            apply_basic_markup()

            print(f'🦇 datafile created at {DATA_PATH}')
            print('basic markup applied')
            exit(0)
        else:
            exit(1)


# custom methods

def get_tags() -> list:
    data = read_data()
    tags: list = get_field(data, 'tags')

    return tags if tags else []

def get_sessions() -> list[dict]:
    data = read_data()
    sessions: list = get_field(data, 'sessions')

    return sessions if sessions else []

def get_active_session() -> dict | None:
    data = read_data()
    active_session = get_field(data, 'active_session')

    return active_session
