"""Defines error messages and functions."""

_BAD_NAME = "Bad name '{name}'."


class CheckError(Exception):

    def __init__(self, message):
        self.message = message


def bad_name(name):
    _error(_BAD_NAME, name=name)


def _error(message, **keywords):
    raise CheckError(message.format_map(keywords))
