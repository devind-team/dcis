"""Скрипт генерирующий markdown файлы по docstring."""
import os
import re
from typing import cast

import django
import pdoc
from django.db.models.query_utils import DeferredAttribute
from django.db.models.manager import ManagerDescriptor
from snakemd import Document, Table

# Specify settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devind.settings')
# Setup Django
django.setup()


def recursive_module(mod: pdoc.doc.Module):
    """Рекурсия прохождения по всем модулям."""




    yield mod
    for submod in mod.submodules:
        yield from recursive_module(submod)


def get_function(module_functions: list) -> list:
    """Извлечение данных функции из модуля."""
    list_functions = []
    for module_function in module_functions:
        function = {
            'name': module_function.name,
            'docstring': remove_symbol(module_function.docstring),
            'decorators': [re.sub('@', '', decorator) for decorator in module_function.decorators],
            'signature': remove_symbol(str(module_function.signature)).replace('|', '&#124;'),
        }
        list_functions.append(function)
    return list_functions


def get_class(module_classes: list) -> list:
    """Извлечение данных класса из модуля."""
    list_classes = []
    for module_class in module_classes:
        clazz = {
            'name': module_class.name,
            'docstring': module_class.docstring,
            'methods': get_methods(module_class),
        }
        list_classes.append(clazz)
    return list_classes


def is_method(member: pdoc.doc.Doc) -> bool:
    return isinstance(member, pdoc.doc.Function) and not any((
        isinstance(member.obj, DeferredAttribute),
        isinstance(member.obj, ManagerDescriptor),
    )) and str(member.signature) != '(unknown)'


def is_magic(attr_name: str) -> bool:
    """Проверка является ли атрибут магическим."""
    return f'__{attr_name[2:-2]}__' == attr_name


def is_private(attr_name: str) -> bool:
    """Проверка является ли атрибут приватным."""
    return (attr_name[0] == '_' or attr_name[0:1] == '__') and not is_magic(attr_name)


def get_methods(module_class: pdoc.doc.Class) -> list:
    """Извлечение данных метода класса."""
    list_methods = []
    for own_member in module_class.own_members:
        if is_method(own_member) and not is_private(own_member.name):
            own_member = cast(pdoc.doc.Function, own_member)
            methods = {
                'name': own_member.name,
                'docstring': remove_symbol(own_member.docstring),
                'decorators': [re.sub('@', '', decorator) for decorator in own_member.decorators],
                'signature': remove_symbol(str(own_member.signature)).replace('|', '&#124;'),
            }
            list_methods.append(methods)
    return list_methods


def remove_symbol(string: str) -> str:
    """Преобразование в строку и удаление лишних символов."""
    return re.sub(' +', ' ', string.replace('\n', '')).replace('<', '&#60;').replace('>', '&#62;')


def generate_markdown(mod: pdoc.doc.Module):
    """Генерация markdown файла."""
    doc = Document(f'{mod.source_file.stem}')
    doc.add_header(text=f'Модуль {mod.name}', level=1)
    doc.add_paragraph(text=f'{mod.docstring}')
    if mod.functions:
        doc.add_header(text=f'Функции', level=3)
        doc.add_table(
            ['Сигнатура', 'Декораторы', 'Описание'],
            [
                [f"{function['name']}{function['signature']}",
                 f"{'-' if not function['decorators'] else ', '.join(function['decorators'])}",
                 f"{'-' if not function['docstring'] else function['docstring']}"]
                for function in get_function(mod.functions)
            ],
            [Table.Align.LEFT, Table.Align.LEFT, Table.Align.LEFT]
        )
    if mod.classes:
        for clazz in get_class(mod.classes):
            doc.add_header(text=f"Класс {clazz['name']}", level=2)
            doc.add_paragraph(text=f"{clazz['docstring']}")
            if clazz['methods']:
                doc.add_header(text=f'Методы', level=3)
                doc.add_table(
                    ['Сигнатура', 'Декораторы', 'Описание'],
                    [
                        [f"{method['name']}{method['signature']}",
                         f"{'-' if not method['decorators'] else ', '.join(method['decorators'])}",
                         f"{'-' if not method['docstring'] else method['docstring']}"]
                        for method in clazz['methods']
                    ],
                    [Table.Align.LEFT, Table.Align.LEFT, Table.Align.LEFT]
                )
    doc.output_page(
        dump_dir=os.path.join(str(mod.source_file.parent).replace('server\\apps', 'docs\\api\\server')),
        encoding='utf-8'
    )


def main() -> None:
    """Скрипт генерирующий markdown файлы по docstring."""
    for module in (pdoc.doc.Module.from_name('apps')).submodules:
        for mod_module in recursive_module(module):
            if not mod_module.submodules and not ('migrations' in mod_module.fullname):
                generate_markdown(mod_module)


if __name__ == '__main__':
    main()
