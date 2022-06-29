"""Скрипт генерирующий markdown файлы по docstring"""
import os
import sys
import django
import pdoc
import re
from devind.settings import BASE_DIR
from snakemd import Table, Document


# sys.path.append(os.path.abspath('../server/'))  # path to your django project
# Specify settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devind.settings')
# Setup Django
django.setup()


def recursive_module(mod: pdoc.doc.Module):
    """Рекурсия прохождения по всем модулям"""
    yield mod
    for submod in mod.submodules:
        yield from recursive_module(submod)


def get_function(module_functions: list) -> list:
    """Извлечение данных функции из модуля"""
    list_functions = []
    for module_function in module_functions:
        function = {
            'name': module_function.name,
            'docstring': remove_symbol(module_function.docstring),
            'decorators': module_function.decorators,
            'signature': remove_symbol(str(module_function.signature)),
        }
        list_functions.append(function)
    return list_functions


def get_class(module_classes: list) -> list:
    """Извлечение данных класса из модуля"""
    list_classes = []
    for module_class in module_classes:
        clazz = {
            'name': module_class.name,
            'docstring': module_class.docstring,
            'methods': get_methods(module_class),
        }
        list_classes.append(clazz)
    return list_classes


def get_methods(module_class: pdoc.doc.Class) -> list:
    """Извлечение данных метода класса"""
    list_methods = []
    for own_member in module_class.own_members:
        if isinstance(own_member, pdoc.doc.Function) and (own_member.name[0] != '_'
                                                          or ('__' in own_member.name)):
            methods = {
                'name': own_member.name,
                'docstring': remove_symbol(own_member.docstring),
                'decorators': own_member.decorators,
                'signature': remove_symbol(str(own_member.signature)),
            }
            list_methods.append(methods)
    return list_methods


def remove_symbol(string: str) -> str:
    """Преобразование в строку и удаление лишних символов"""
    return re.sub(' +', ' ', string.replace('\n', ''))


def generate_markdown(mod: pdoc.doc.Module):
    """Генерация markdown файла"""
    doc = Document(f'{mod.source_file.stem}')
    doc.add_header(text=f'Модуль {mod.name}', level=1)
    doc.add_paragraph(text=f'{mod.docstring}')
    if mod.functions:
        doc.add_header(text=f'Функции', level=3)
        doc.add_table(
            ['Signature', 'Decorator', 'Docstring'],
            [
                [f"{function['name']}{function['signature']}",
                 f"{'-' if not function['decorators'] else function['decorators']}",
                 f"{'-' if not function['docstring'] else function['docstring']}"]
                for function in get_function(mod_module.functions)
            ],
            [Table.Align.LEFT, Table.Align.LEFT, Table.Align.LEFT]
        )
    if mod_module.classes:
        for clazz in get_class(mod_module.classes):
            doc.add_header(text=f"Класс {clazz['name']}", level=2)
            doc.add_paragraph(text=f"{clazz['docstring']}")
            if clazz['methods']:
                doc.add_header(text=f'Методы', level=3)
                doc.add_table(
                    ['Signature', 'Decorator', 'Docstring'],
                    [
                        [f"{method['name']}{method['signature']}",
                         f"{'-' if not method['decorators'] else method['decorators']}",
                         f"{'-' if not method['docstring'] else method['docstring']}"]
                        for method in clazz['methods']
                    ],
                    [Table.Align.LEFT, Table.Align.LEFT, Table.Align.LEFT]
                )
    doc.output_page(dump_dir=os.path.join(str(mod.source_file.parent).replace('server', 'docs\\api')), encoding='utf-8')


for module in (pdoc.doc.Module.from_name('apps')).submodules:
# for module in (pdoc.doc.Module.from_name(BASE_DIR.name)).submodules:
    for mod_module in recursive_module(module):
        if not mod_module.submodules and not ('migrations' in mod_module.fullname):
            generate_markdown(mod_module)
