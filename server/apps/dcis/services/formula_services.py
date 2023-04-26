"""Модуль, отвечающий за работу с формулами."""

TRANSLATED_FUNCTIONS = {
    'ABS': 'ABS',
    'ACOS': 'ACOS',
    'ACOSH': 'ACOSH',
    'ASIN': 'ASIN',
    'ASINH': 'ASINH',
    'ATAN2': 'ATAN2',
    'ATAN': 'TAN',
    'CEILING': 'ОКРВВЕРХ',
    'COSH': 'COSH',
    'COS': 'COS',
    'DEGREES': 'ГРАДУСЫ',
    'EVEN': 'ЧЁТН',
    'EXP': 'EXP',
    'FACT': 'ФАКТР',
    'FACTDOUBLE': 'ДВФАКТР',
    'FLOOR': 'ОКРВНИЗ',
    'INT': 'ЦЕЛОЕ',
    'LN': 'LN',
    'LOG10': 'LOG10',
    'LOG': 'LOG',
    'MOD': 'ОСТАТ',
    'PI': 'ПИ',
    'POWER': 'СТЕПЕНЬ',
    'RADIANS': 'РАДИАНЫ',
    'RANDBETVEEN': 'СЛУЧМЕЖДУ',
    'RAND': 'СЛЧИС',
    'ROUNDDOWN': 'ОКРУГЛВНИЗ',
    'ROUNDUP': 'ОКРУГЛВВЕРХ',
    'ROUND': 'ОКРУГЛ',
    'SIGN': 'ЗНАК',
    'SIN': 'SIN',
    'SQRTPI': 'КОРЕНЬПИ',
    'SQRT': 'КОРЕНЬ',
    'SUMIFS': 'СУММЕСЛИМН',
    'SUMIF': 'СУММЕСЛИ',
    'SUMPRODUCT': 'СУММПРОИЗВ',
    'SUM': 'СУММ',
    'TAN': 'TAN',
    'TRUNC': 'ОТБР',
    'AVERAGE': 'СРЗНАЧ',
    'COUNTA': 'СЧЁТЗ',
    'COUNTIFS': 'СЧЁТЕСЛИМН',
    'COUNTIF': 'СЧЁТЕСЛИ',
    'COUNT': 'СЧЁТ',
    'MAX': 'МАКС',
    'MIN': 'МИН',
    'CONCAT': 'СЦЕПИТЬ',
    'EXACT': 'СОВПАД',
    'FIND': 'НАЙТИ',
    'LEFT': 'ЛЕВСИМВ',
    'LEN': 'ДЛСТР',
    'LOWER': 'СТРОЧН',
    'MID': 'ПСТР',
    'REPLACE': 'ЗАМЕНИТЬ',
    'RIGHT': 'ПРАВСИМВ',
    'TRIM': 'СЖПРОБЕЛЫ',
    'UPPER': 'ПРОПИСН',
    'VALUE': 'ЗНАЧЕН',
    'CHOOSE': 'ВЫБОР',
    'MATCH': 'ПОИСКПОЗ',
    'VLOOKUP': 'ВПР',
    'AND': 'И',
    'FALSE': 'ЛОЖЬ',
    'IF': 'ЕСЛИ',
    'OR': 'ИЛИ',
    'TRUE': 'ИСТИНА',
    'ISBLANK': 'ЕПУСТО',
    'ISERROR': 'ЕОШИБКА',
    'ISERR': 'ЕОШ',
    'ISEVEN': 'ЕЧЁТН',
    'ISNA': 'ЕНД',
    'ISNUMBER': 'ЕЧИСЛО',
    'ISODD': 'ЕНЕЧЁТ',
    'ISTEXT': 'ЕТЕКСТ',
    'NA': 'НД',
    'IRR': 'ВСД',
    'NPV': 'ЧПС',
    'PMT': 'ПЛТ',
    'PV': 'ПС',
    'SLN': 'АПЛ',
    'VDB': 'ПУО',
    'XIRR': 'ЧИСТВНДОХ',
    'XNPV': 'ЧИСТНЗ',
    'BIN2DEC': 'ДВ.В.ДЕС',
    'BIN2HEX': 'ДВ.В.ШЕСТН',
    'BIN2OCT': 'ДВ.В.ВОСЬМ',
    'DEC2BIN': 'ДЕС.В.ДВ',
    'DEC2HEX': 'ДЕС.В.ШЕСТН',
    'DEC2OCT': 'ДЕС.В.ВОСЬМ',
    'HEX2BIN': 'ШЕСТН.В.ДВ',
    'HEX2DEC': 'ШЕСТН.В.ДЕС',
    'HEX2OCT': 'ШЕСТН.В.ВОСЬМ',
    'OCT2BIN': 'ВОСЬМ.В.ДВ',
    'OCT2DEC': 'ВОСЬМ.В.ДЕС',
    'OCT2HEX': 'ВОСЬМ.В.ШЕСТН',
    'DATEVALUE': 'ДАТАЗНАЧ',
    'DAYS': 'ДНИ',
    'DAY': 'ДЕНЬ',
    'EDATE': 'ДАТАМЕС',
    'DATEDIF': 'РАЗНДАТ',
    'DATE': 'ДАТА',
    'EOMONTH': 'КОНМЕСЯЦА',
    'ISOWEEKNUM': 'НОМНЕДЕЛИ.ISO',
    'MONTH': 'МЕСЯЦ',
    'NOW': 'ТДАТА',
    'TODAY': 'СЕГОДНЯ',
    'WEEKDAY': 'ДЕНЬНЕД',
    'YEARFRAC': 'ДОЛЯГОДА',
    'YEAR': 'ГОД'
}


def translate_formula_en2ru(formula: str) -> str:
    """Перевод формулы с английского на русский."""
    for en, ru in TRANSLATED_FUNCTIONS.items():
        formula = formula.replace(en, ru)
    result = ''
    is_quote = False
    for char in formula:
        if char == '"':
            is_quote = not is_quote
        if not is_quote:
            char = ';' if char == ',' else char
            char = ',' if char == '.' else char
        result += char
    return result


def translate_formula_ru2en(formula: str) -> str:
    """Перевод формулы с русского на английский."""
    for en, ru in TRANSLATED_FUNCTIONS.items():
        formula = formula.replace(ru, en)
    result = ''
    is_quote = False
    for char in formula:
        if char == '"':
            is_quote = not is_quote
        if not is_quote:
            if char == ';':
                char = ','
            elif char == ',':
                char = '.'
        result += char
    return result
