from . import errors
from .objects import *  # noqa: F401,F403
from . import _checker
from . import _generator
from ._new_generator import *


CheckError = errors.CheckError


def check(ast_):
    _checker.main(ast_)


def generate(ast_):
    return _generator.main(ast_)
