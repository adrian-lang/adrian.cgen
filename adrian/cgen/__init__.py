from . import errors
from . import objects
from . import _checker
from . import _generator


CheckError = errors.CheckError


def check(ast_):
    _checker.main(ast_)


def generate(ast_):
    return _generator.main(ast_)
