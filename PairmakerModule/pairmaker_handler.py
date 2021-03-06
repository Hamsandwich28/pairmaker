import re
import flask
from typing import Optional

from pairmaker_answer_stringify import NumberToString

amount = {
    'beard': 4,
    'brows': 20,
    'hair': 13,
    'eyes': 24,
    'lips': 3,
    'nose': 5,
    'addition': 1
}


def check_link_on_sql(link: str) -> bool:
    if link == "":
        return True
    sql_words = [
        "add constraint", "alter", "alter column", "alter table", "backup database", "between", "case", "check",
        "column", "constraint", "create", "create database", "create index", "create or replace view", "create table",
        "create procedure", "create unique index", "create view", "database", "default", "delete", "distinct",
        "drop", "drop column", "drop constraint", "drop database", "drop default", "drop index", "drop table",
        "drop view", "exec", "exists", "foreign key", "from", "full outer join", "group by", "having", "index",
        "inner join", "insert into", "insert into select", "is null", "is not null", "join", "left join",
        "limit", "not null", "order by", "outer join", "primary key", "procedure", "postgre", "postgres", "postgresql",
        "right join", "rownum", "select", "select distinct", "select into", "select top", "table", "truncate table",
        "union", "union all", "unique", "update", "values", "view", "where", "version"
    ]
    link = link.lower()
    for sql in sql_words:
        if sql in link:
            return False
    return True


def sqlescape(str):
    return str.translate(
        str.maketrans({
            "\0": "\\0",
            "\r": "\\r",
            "\x08": "\\b",
            "\x09": "\\t",
            "\x1a": "\\z",
            "\n": "\\n",
            "\"": "",
            "'": "",
            "\\": "\\\\",
            "%": "\\%"
        }))


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
    try:
        ext = filename.split('.')[-1]
        if ext.lower() in ['png', 'jpg']:
            return True
    except Exception:
        pass
    return False


def _request_form_getter(req: flask.Request, keyword: str) -> list:
    return [
        req.form.get(k)
        for k in req.form.keys()
        if keyword in k
    ]


def _request_identikit_parser(req: flask.Request) -> dict:
    return {k: v for k, v in req.form.items()}


def _get_base_data_str(base_data: tuple) -> dict:
    return {
        'name': base_data[1],
        'links': {
            'link_vk': {
                'title': '??????????????????',
                'value': base_data[8]
            },
            'link_inst': {
                'title': '??????????????????',
                'value': base_data[9]
            },
            'link_num': {
                'title': '??????????????',
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
            'title': '??????',
            'value': NumberToString.get_user_gender(base_data[4])
        },
        'age': {
            'title': '??????????????',
            'value': NumberToString.get_user_age(base_data[5])
        },
        'growth': {
            'title': '????????',
            'value': NumberToString.get_user_growth(base_data[6])
        },
        'sport': {
            'title': '?????????????????? ?? ????????????',
            'value': NumberToString.get_form_sport(form_data[1])
        },
        'hobby': {
            'title': '?????????????? ??????????????',
            'value': NumberToString.get_hobby_str(form_data[2], form_data[3])
        },
        'movie': {
            'title': '?????????????? ?????????? ??????????????',
            'value': NumberToString.get_movie_str(form_data[4], form_data[5])
        },
        'lit': {
            'title': '?????????????? ?????????? ????????????????????',
            'value': NumberToString.get_lit_str(form_data[6], form_data[7])
        }
    }
    return result
