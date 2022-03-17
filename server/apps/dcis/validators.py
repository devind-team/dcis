from devind_helpers.validator import Validator


class ProjectValidator(Validator):
    name = 'required|min_length:2|max_length:250'
    short = 'required|min_length:2|max_length:30'
    description = 'required|min_length:2|max_length:1023'
