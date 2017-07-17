from . import errors
from .objects import *  # noqa: F401,F403
from . import _checker
from ._generator import *


CheckError = errors.CheckError


class Generator:

    def __init__(self):
        self.ast_list = []
        self.generator = NodeGenerator()

    def add_ast(self, ast_):
        self.ast_list.append(ast_)

    def generate_ast(self, ast_):
        result = Generated()
        for node in ast_:
            result.merge(self.generator.generate(node))
        return result

    def generate(self):
        result = Generated()
        for ast_ in self.ast_list:
            result.merge(self.generate_ast(ast_))
        for line in result.to_csource():
            yield line


def check(ast_):
    _checker.main(ast_)


def generate(ast_):
    return _generator.main(ast_)
