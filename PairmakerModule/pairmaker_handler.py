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


def _check_link_format(link: str) -> bool:
    # re
    return True
