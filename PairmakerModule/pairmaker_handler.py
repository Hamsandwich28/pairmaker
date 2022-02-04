import re
import flask
from typing import Optional

from pairmaker_answer_stringify import NumberToString

url_re = '(https?://[^\"\s>]+)'
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
    if re.match(url_re, link):
        return True
    return False


def _construct_dict_from_user_form(data: tuple) -> dict:
    return {
        'sport': data[1],
        'hobby1': data[2],
        'hobby2': data[3],
        'movie1': data[4],
        'movie2 ': data[5],
        'lit1': data[6],
        'lit2': data[7]
    }


def _identikit_tuple_to_dict(data: list) -> dict:
    return {
        'brows': data[1],
        'eyes': data[2],
        'hair': data[3],
        'lips': data[4],
        'nose': data[5],
        'beard': data[6],
        'addition': data[7]
    }


def _get_user_full_data(user_data: list,
                        social_data: Optional[str],
                        identikit_data: list,
                        form_data: list) -> dict:
    return {
        'userdata': {
            'name': {
                'title': 'Имя',
                'value': user_data[0],
            },
            'ismale': {
                'title': 'Пол',
                'value': NumberToString.get_user_gender(user_data[1])
            },
            'age': {
                'title': 'Возраст',
                'value': NumberToString.get_user_age(user_data[2])
            },
            'growth': {
                'title': 'Рост',
                'value': NumberToString.get_user_growth(user_data[3])
            }
        },
        'identikit': _identikit_tuple_to_dict(identikit_data),
        'formdata': {
            'sport': {
                'title': 'Отношение к спорту',
                'value': NumberToString.get_form_sport(form_data[1])
            },
            'hobby': {
                'title': 'Мои увлечения',
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
        },
        'socialdata': {
            'social': {
                'title': 'Связь с пользователем',
                'value': social_data
            }
        }
    }
