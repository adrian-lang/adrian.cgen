from . import errors
from .objects import *  # noqa: F401,F403
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
        subresult = Generated()
        for ast_ in self.ast_list:
            subresult.merge(self.generate_ast(ast_))
        yield from subresult.to_csource()
