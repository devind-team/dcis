import os
import sys
import django
import pdoc
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
            'docstring': module_function.docstring,
            'decorators': module_function.decorators,
            'signature': str(module_function.signature),
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
                'signature': str(own_member.signature),
            }
            list_methods.append(methods)
    return list_methods


for module in (pdoc.doc.Module.from_name('apps.core')).submodules:
# for module in (pdoc.doc.Module.from_name(BASE_DIR.name)).submodules:
    begin = module
    if not ('migrations' in module.fullname):
        for mod_module in recursive_module(module):
            if not mod_module.submodules:
                print(mod_module.source_file)
                if mod_module.functions:
                    functions = get_function(mod_module.functions)
                if mod_module.classes:
                    clazz = classes = get_class(mod_module.classes)
                    print(clazz)
                # print(TEMPLATE.render(module=mod_module))
                # with open(f"./docs/{module_name}.md", "w", encoding="utf8") as f:
                #     f.write(TEMPLATE.render(module=mod_module))


# modules = [pdoc.Module(mod, context=context)
#            for mod in modules]
# pdoc.link_inheritance(context)
#
#
# def recursive_htmls(mod):
#     yield mod.name, mod.text()
#     for submod in mod.submodules():
#         yield from recursive_htmls(submod)
#
#
# for mod in modules:
#     for module_name, html in recursive_htmls(mod):
#         print(html)
#         with open(f"./docs/{module_name}.md", "w", encoding="utf8") as f:
#             f.write(html)
