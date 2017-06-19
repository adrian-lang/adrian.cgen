from . import errors
from .objects import *  # noqa: F401,F403
from . import _checker
from ._generator import *


CheckError = errors.CheckError


# class Generated:

#     def __init__(self):
#         # self.includes = {}
#         self.includes = []
#         self.func_signs = []
#         self.rest_code = []

#     def to_csource(self):
#         general_list = self.includes + self.func_signs + self.rest_code
#         for line in general_list:
#             yield line

#     def _merge_includes(self, includes):
#         for include in includes:
#             in_includes = False
#             for incl in self.includes:
#                 if include.module_name == incl.module_name:
#                     in_includes = True
#             if not in_includes:
#                 self.includes.append(include)

#     def _merge_func_signs(self, func_signs):
#         for func_sign in func_signs:
#             self.func_signs.append(func_sign)

#     def _merge_rest_code(self, rest_code):
#         for code_stmt in rest_code:
#             self.rest_code.append(code_stmt)

#     def merge(self, generated):
#         self._merge_includes(generated.includes)
#         self._merge_func_signs(generated.func_signs)
#         self._merge_rest_code(generated.rest_code)


class Generator:

    def __init__(self):
        self.ast_list = []
        self.generator = NodeGenerator()

    def add_ast(self, ast_):
        self.ast_list.append(ast_)

    def generate_ast(self, ast_):
        for node in ast_:
            yield self.generator.generate(node)
        # result = Generated()
        # for node in ast_:
        #     result.merge(self.generator.generate(node))
        # return result

    def generate(self):
        result = []
        for ast_ in self.ast_list:
            result.extend(self.generate_ast(ast_))
        # result = Generated()
        # for ast_ in self.ast_list:
        #     result.merge(self.generate_ast(ast_))
        for line in result:
            yield line


def check(ast_):
    _checker.main(ast_)


def generate(ast_):
    return _generator.main(ast_)
