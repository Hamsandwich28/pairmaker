from typing import Optional


class NumberToString:
    placeholder = 'Не определено'
    _num_to_age = {
        '0': 'до 23 лет',
        '1': 'от 23 до 27 лет',
        '2': 'от 27 до 32 лет',
        '3': 'от 32 до 37 лет',
        '4': 'от 37 лет и старше'
    }
    _num_to_growth = {
        '0': 'до 165 см',
        '1': 'от 165 до 172 см',
        '2': 'от 172 до 178 см',
        '3': 'от 178 см и выше'
    }
    _num_to_sport = {
        '0': 'Не увлекаюсь спортом',
        '1': 'Я скорее болельщик',
        '2': 'Отличное, регулярно занимаюсь'
    }
    _num_to_hobby = {
        '0': 'Рисую',
        '1': 'Пою',
        '2': 'Танцую',
        '3': 'Играю на музыкальном инструменте',
        '4': 'Увлекаюсь туризмом',
        '5': 'Катаюсь на сноуборде',
        '6': 'Катаюсь на горных лыжах',
        '7': 'Коллекционирую что-либо',
        '8': 'Много путешествую',
        '9': 'Катаюсь на коньках',
        '10': 'Катаюсь на велосипеде',
        '11': 'Занимаюсь йогой',
        '12': 'Вяжу',
        '13': 'Вышиваю',
        '14': 'Делаю поделки'
    }
    _num_to_movie = {
        '0': 'Комедия',
        '1': 'Боевик',
        '2': 'Ужасы',
        '3': 'Триллер',
        '4': 'Драма',
        '5': 'Мелодрама',
        '6': 'Детектив',
        '7': 'Фантастика',
        '8': 'Мюзикл',
        '9': 'Приключения',
        '10': 'Аниме',
        '11': 'Мультфильм'
    }
    _num_to_lit = {
        '0': 'Фантастика',
        '1': 'Роман',
        '2': 'Поэзия',
        '3': 'Научная литература',
        '4': 'Комикс',
        '5': 'Бизнес литература',
        '6': 'Историческая литература',
        '7': 'Биография',
        '8': 'Детектив',
        '9': 'Сатира'
    }

    @classmethod
    def get_user_gender(cls, ismale: int) -> str:
        return 'Мужской' if ismale == 1 else 'Женский'

    @classmethod
    def get_user_age(cls, agenum: int) -> str:
        return cls._num_to_age[str(agenum)] if agenum is not None else cls.placeholder

    @classmethod
    def get_user_growth(cls, growthnum: int) -> str:
        return cls._num_to_growth[str(growthnum)] if growthnum is not None else cls.placeholder

    @classmethod
    def get_form_sport(cls, sportnum: int) -> str:
        return cls._num_to_sport[str(sportnum)] if sportnum is not None else cls.placeholder

    @classmethod
    def get_form_hobby(cls, hobbynum: int) -> str:
        return cls._num_to_hobby[str(hobbynum)] if hobbynum is not None else cls.placeholder

    @classmethod
    def get_form_movie(cls, movienum: int) -> str:
        return cls._num_to_movie[str(movienum)] if movienum is not None else cls.placeholder

    @classmethod
    def get_form_lit(cls, litnum: int) -> str:
        return cls._num_to_lit[str(litnum)] if litnum is not None else cls.placeholder

    @classmethod
    def get_hobby_str(cls, value1: int, value2: Optional[int]) -> str:
        if value1 is None:
            return cls.placeholder
        if value2 is not None:
            return f"{NumberToString.get_form_hobby(value1)}, {NumberToString.get_form_hobby(value2)}"
        return f"{NumberToString.get_form_hobby(value1)}"

    @classmethod
    def get_movie_str(cls, value1: int, value2: Optional[int]) -> str:
        if value1 is None:
            return cls.placeholder
        if value2 is not None:
            return f"{NumberToString.get_form_movie(value1)}, {NumberToString.get_form_movie(value2)}"
        return f"{NumberToString.get_form_movie(value1)}"

    @classmethod
    def get_lit_str(cls, value1: int, value2: Optional[int]) -> str:
        if value1 is None:
            return cls.placeholder
        if value2 is not None:
            return f"{NumberToString.get_form_lit(value1)}, {NumberToString.get_form_lit(value2)}"
        return f"{NumberToString.get_form_lit(value1)}"


class IdentikitPathBuilder:
    basepath = 'img'
    extension = 'png'
    common_types = ['brows', 'eyes', 'hair', 'lips', 'nose']

    @classmethod
    def _get_common_path(cls, part: str, value: int, ismale: bool) -> str:
        gender_prefix = 'm' if ismale else 'f'
        return f"{cls.basepath}/{part}/{gender_prefix}/{part}{value}.{cls.extension}"

    @classmethod
    def _get_uncommon_path(cls, part: str, value: int, ismale: bool) -> str:
        if part == 'beard' and not ismale:
            raise ValueError("Неверный тип части тела!")

        return f"{cls.basepath}/{part}/{part}{value}.{cls.extension}"

    @classmethod
    def construct_image_paths(cls, identikit_data: dict, ismale: bool) -> dict:
        result = {}
        for part, value in identikit_data.items():
            if part in cls.common_types:
                result[part] = cls._get_common_path(part, value, ismale)
            elif value:
                result[part] = cls._get_uncommon_path(part, value, ismale)
        return result
