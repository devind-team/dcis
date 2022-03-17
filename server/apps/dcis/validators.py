from devind_helpers.validator import Validator


class ProjectValidator(Validator):
    name = 'required|min_length:2|max_length:250'
    short = 'required|min_length:2|max_length:30'
    description = 'required|min_length:2|max_length:1023'

    message = {
        'name': {
            'required': 'Поле "Название проекта" обязательное для заполнения',
            'min_length': 'Минимальная длина 2 символа',
            'max_length': 'Максимальная длина не более 250 символов'
        },
        'short': {
            'required': 'Поле "Короткое название проекта" обязательное для заполнения',
            'min_length': 'Минимальная длина 2 символа',
            'max_length': 'Максимальная длина не более 30 символов'
        },
        'description': {
            'required': 'Поле "Описание проекта" обязательное для заполнения',
            'min_length': 'Минимальная длина 2 символа',
            'max_length': 'Максимальная длина не более 1023 символов'
        }
    }
