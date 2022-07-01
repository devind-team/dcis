# Модуль info_fields

Get requested fields from ResolveInfo. https://gist.github.com/mixxorz/dc36e180d1888629cf33

### Функции

| Signature                       | Decorator | Docstring                                                                                                                                                                                                                                                                                  |
| :------------------------------ | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| collect_fields(node, fragments) | -         | Recursively collects fields from the ASTArgs: node (dict): A node in the AST fragments (dict): Fragment definitionsReturns: A dict mapping each field found, along with their sub fields. {'name': {}, 'sentimentsPerLanguage': {'id': {}, 'name': {}, 'totalSentiments': {}}, 'slug': {}} |
| get_fields(info)                | -         | A convenience function to call collect_fields with infoArgs: info (ResolveInfo)Returns: dict: Returned from collect_fields                                                                                                                                                                 |