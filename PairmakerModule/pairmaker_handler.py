import re
import flask
from typing import Optional

from pairmaker_answer_stringify import NumberToString

# '(https?://[^\"\s>]+)'
masks = ['https://vk.com/', 'https://www.instagram.com/', r'(\d{11})']
amount = {
    'beard': 4,
    'brows': 20,
    'hair': 13,
    'eyes': 24,
    'lips': 3,
    'nose': 5,
    'addition': 1
}


def _key_values_dict(obj: list, basename: str, amount: int) -> dict:
    result = {
        basename + str(1): None,
        basename + str(2): None
    }
    posted = 0
    for row in obj:
        if row:
            result[basename + str(posted + 1)] = row
            posted += 1
        if posted == amount:
            break
    return result


def _check_img_format(filename: str) -> bool:
    ext = filename.split('.', 1)[1]
    if ext.lower() in ['png', 'jpg']:
        return True
    return False


def _request_form_getter(req: flask.Request, keyword: str) -> list:
    return [
        req.form.get(k)
        for k in req.form.keys()
        if keyword in k
    ]


def _request_identikit_parser(req: flask.Request) -> dict:
    return {k: v for k, v in req.form.items()}


def _check_link_format(link: str) -> bool:
    if masks[0] in link or masks[1] in link or re.match(masks[2], link):
        return True
    return False


def _get_base_data_str(base_data: tuple) -> dict:
    return {
        'name': base_data[1],
        'links': {
            'link_vk': {
                'title': 'Вконтакте',
                'value': base_data[8]
            },
            'link_inst': {
                'title': 'Инстраграм',
                'value': base_data[9]
            },
            'link_num': {
                'title': 'Телефон',
                'value': base_data[10]
            }
        }
    }


def _get_kit_data_str(kit_data: tuple) -> dict:
    return {
        'brows': kit_data[1],
        'eyes': kit_data[2],
        'hair': kit_data[3],
        'lips': kit_data[4],
        'nose': kit_data[5],
        'beard': kit_data[6],
        'addition': kit_data[7]
    }


def _get_form_data_str(form_data: tuple, base_data: tuple) -> dict:
    result = {
        'gender': {
            'title': 'Пол',
            'value': NumberToString.get_user_gender(base_data[4])
        },
        'age': {
            'title': 'Возраст',
            'value': NumberToString.get_user_age(base_data[5])
        },
        'growth': {
            'title': 'Рост',
            'value': NumberToString.get_user_growth(base_data[6])
        },
        'sport': {
            'title': 'Отношение к спорту',
            'value': NumberToString.get_form_sport(form_data[1])
        },
        'hobby': {
            'title': 'Любимые занятия',
            'value': NumberToString.get_hobby_str(form_data[2], form_data[3])
        },
        'movie': {
            'title': 'Любимые жанры фильмов',
            'value': NumberToString.get_movie_str(form_data[4], form_data[5])
        },
        'lit': {
            'title': 'Любимые жанры литературы',
            'value': NumberToString.get_lit_str(form_data[6], form_data[7])
        }
    }
    return result
