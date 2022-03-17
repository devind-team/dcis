from devind_helpers.validator import Validator


class ProjectValidator(Validator):
    name = 'required|min_length:2|max_length:250'
    short = 'required|min_length:2|max_length:30'
    description = 'required|min_length:2|max_length:1023'

    message = {
        'name': {
            'required': 'Поле обязательное для заполнения',
            'min_length': 'Минимальная длина не менее 3 символов',
            'max_length': 'Максимальная длина не более 1023 символов'
        },
        'short': {
            'required': 'Поле обязательное для заполнения',
            'min_length': 'Минимальная длина не менее 3 символов',
            'max_length': 'Максимальная длина не более 1023 символов'
        },
        'description': {
            'required': 'Поле обязательное для заполнения',
            'min_length': 'Минимальная длина не менее 3 символов',
            'max_length': 'Максимальная длина не более 1023 символов'
        },
    }
