"""Defines error messages and functions."""

_BAD_NAME = "Bad name '{name}'."
_BAD_LITERAL = "Bad literal '{literal}'."

_NOT_IMPLEMENTED = "Not implemented."


class CheckError(Exception):

    def __init__(self, message):
        self.message = message


def bad_name(name):
    _error(_BAD_NAME, name=name)


def bad_literal(literal):
    _error(_BAD_LITERAL, literal=literal)


def not_implemented():
    _error(_NOT_IMPLEMENTED)


def _error(message, **keywords):
    raise CheckError(message.format_map(keywords))
