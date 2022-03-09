from devind_helpers.validator import Validator


class CategoryValidator(Validator):
    text = 'required|min_length:3|max_length:1023'
    parent_id = 'exist:pages.Category,id'
    user_id = 'exist:core.User,id'

    message = {
        'text': {
            'required': 'Поле "Название категории" обязательное для заполнения',
            'min_length': 'Минимальная длина не менее 3 символов',
            'max_length': 'Максимальная длина не более 1023 символов'
        },
        'parent_id': {
            'exist': 'Такой категории не существует'
        },
        'user_id': {
            'exist': 'Такого пользователя не существует'
        }
    }


class PageValidator(Validator):
    title = 'required|min_length:3|max_length:1023'
    signature = 'min_length:2|max_length:100'
    category_id = 'exist:pages.Category,id'
    user_id = 'exist:core.User,id'
    kind_id = 'exist:pages.PageKind,id'

    message = {
        'title': {
            'required': 'Поле "Заголовок страницы" обязательное для заполнения',
            'min_length': 'Минимальная длина не менее 3 символов',
            'max_length': 'Максимальная длина не более 1023 символов'
        },
        'signature': {
            'min_length': 'Минимальная длина не менее 3 символов',
            'max_length': 'Максимальная длина не более 100 символов'
        },
        'category_id': {
            'exist': 'Такой категории не существует'
        },
        'user_id': {
            'exist': 'Такого пользователя не существует'
        },
        'kind_id': {
            'exist': 'Такого типа страницы не существует'
        }
    }


class SectionValidator(Validator):
    text = 'min_length:5'
    user_id = 'exist:core.User,id'
    page_id = 'exist:pages.Page,id'

    message = {
        'text': {
            'min_length': 'Минимальная длина не может быть меньше 5 символов'
        },
        'user_id': {
            'exist': 'Такого пользователя не существует'
        },
        'page_id': {
            'exist': 'Такой страницы не существует'
        }
    }


class TagValidator(Validator):
    name = 'required|min_length:1|max_length:256'
    user_id = 'exist:core.User,id'

    message = {
        'name': {
            'required': 'Поле "Имя" обязательное для заполнения',
            'min_length': 'Минимальная длина не менее 1 символа',
            'max_length': 'Максимальная длина не более 256 символов'
        },
        'user_id': {
            'exist': 'Такого пользователя не существует'
        },
    }
