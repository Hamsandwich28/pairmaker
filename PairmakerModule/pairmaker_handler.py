import re
import flask

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
