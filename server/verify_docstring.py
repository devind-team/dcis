import os
import sys
import django
import pdoc

# sys.path.append(os.path.abspath('../server/'))  # path to your django project
# Specify settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devind.settings')
# Setup Django
django.setup()


def recursive_module(mod: pdoc.doc.Module):
    yield mod
    for submod in mod.submodules:
        yield from recursive_module(submod)


for module in (pdoc.doc.Module.from_name('server')).submodules:
    if not ('migrations' in module.fullname):
        for mod_module in recursive_module(module):
            if not mod_module.docstring:
                print(f'Модуль: {mod_module.name}')
                print(f'Путь к модулю: {mod_module.source_file}')
                print('**************************************************')
                if mod_module.functions:
                    for module_function in mod_module.functions:
                        if not module_function.docstring:
                            print(f'Функция: {module_function.name}')
                            print(f'Путь к функции: {module_function.source_file}')
                            print('**************************************************')
                if mod_module.classes:
                    for module_class in mod_module.classes:
                        classes = module_class
                        if not module_class.docstring:
                            print(f'Класс: {module_class.name}')
                            print(f'Путь к классу: {module_class.source_file}')
                            print('**************************************************')
                        for own_member in module_class.own_members:
                            if isinstance(own_member, pdoc.doc.Function) and (own_member.name[0] != '_'
                                                                              or ('__' in own_member.name)):
                                if not own_member.docstring:
                                    print(f'Метод класса {module_class.name}: {own_member.name}')
                                    print(f'Путь к методу класса: {own_member.source_file}')
                                    print('**************************************************')

