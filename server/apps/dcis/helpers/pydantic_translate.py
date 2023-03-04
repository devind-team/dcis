from pydantic_i18n import PydanticI18n


TRANSLATIONS = {
    "en_US": {
        "field required": "field required",
    },
    "ru_RU": {
        "field required": "обязательное поле",
    }
}

translate = PydanticI18n(TRANSLATIONS)
