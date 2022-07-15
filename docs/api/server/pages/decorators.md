# Модуль decorators



### Функции

| Сигнатура                                                                                                                                        | Декораторы | Описание                                  |
| :----------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :---------------------------------------- |
| translate_model( fields: Iterable[str]) -&#62; Callable[[Type[django.db.models.base.Model]], Type[django.db.models.base.Model]]                  | -          | Перевод модели.:param fields: поля модели |
| translate_type( fields: Iterable[str]) -&#62; Callable[[Type[graphene.types.objecttype.ObjectType]], Type[graphene.types.objecttype.ObjectType]] | -          | Перевод типа.:param fields: поля типа     |