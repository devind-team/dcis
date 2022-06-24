import os
import sys
import django
import pdoc
import re
from devind.settings import BASE_DIR
import jinja2

PATH_TEMPLATE = os.path.join(BASE_DIR, 'templates', 'docs.md.jinja2')
TEMPLATE = jinja2.Template(open(PATH_TEMPLATE, encoding='utf-8').read())

# sys.path.append(os.path.abspath('../server/'))  # path to your django project
# Specify settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devind.settings')
# Setup Django
django.setup()


def recursive_module(mod: pdoc.doc.Module):
    yield mod
    for submod in mod.submodules:
        yield from recursive_module(submod)


def get_function(module_functions: list) -> list:
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
    list_methods = []
    for own_member in module_class.own_members:
        if isinstance(own_member, pdoc.doc.Function) and (own_member.name[0] != '_'
                                                          or ('__' in own_member.name)):
            methods = {
                'name': own_member.name,
                'signature': remove_symbol(str(own_member.signature)),
            }
            list_methods.append(methods)
    return list_methods


def remove_symbol(string: str) -> str:
    return re.sub(' +', ' ', string.replace('\n', ''))


for module in (pdoc.doc.Module.from_name('apps.dcis.models')).submodules:
# for module in (pdoc.doc.Module.from_name(BASE_DIR.name)).submodules:
    begin = module
    if not ('migrations' in module.fullname):
        for mod_module in recursive_module(module):
            if not mod_module.submodules:
                print(mod_module.source_file)
                if mod_module.functions:
                    functions = get_function(mod_module.functions)
                else:
                    functions = []
                if mod_module.classes:
                    clazz = classes = get_class(mod_module.classes)
                else:
                    clazz = []
                # print(clazz)
                print(TEMPLATE.render(module=mod_module, module_function=functions, module_class=clazz))
                with open(os.path.join(BASE_DIR, 'docs', f'{mod_module.name}.md'), 'w', encoding='utf8') as f:
                    f.write(TEMPLATE.render(TEMPLATE.render(module=mod_module, module_function=functions,
                                                            module_class=clazz)))
