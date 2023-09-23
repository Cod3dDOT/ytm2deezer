from typing import Type
import unicodedata
import re


def assert_parameter(parameter, param_types: Type, param_name: str):
    """Asserts that the parameter is of proper type"""
    if not isinstance(parameter, param_types):
        raise TypeError(
            f"{param_name} must be of type {param_types}\n"
            f"{param_name}: {parameter}, type: {type(parameter)}"
        )


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
