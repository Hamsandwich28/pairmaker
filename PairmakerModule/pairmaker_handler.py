import re
import flask
from typing import Optional

from pairmaker_dict import NumberToString

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


def _get_user_full_data(user_data: list, identikit_data: list, form_data: list) -> dict:
    return {
        'userdata': {
            'name': user_data[0],
            'ismale': NumberToString.get_user_gender(user_data[1]),
            'age': NumberToString.get_user_age(user_data[2]),
            'growth': NumberToString.get_user_growth(user_data[3])
        },
        'identikit': {
            'brows': identikit_data[1],
            'eyes': identikit_data[2],
            'hair': identikit_data[3],
            'lips': identikit_data[4],
            'nose': identikit_data[5],
            'beard': identikit_data[6],
            'addition': identikit_data[7],
        },
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
        }
    }