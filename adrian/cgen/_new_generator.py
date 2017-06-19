from paka import funcreg

from . import errors
from . import objects
from . import _context
from . import _layers


class Generated:

    def __init__(self):
        # self.includes = {}
        self.includes = []
        self.func_signs = []
        self.rest_code = []

    def to_csource(self):
        general_list = self.includes + self.func_signs + self.rest_code
        for line in general_list:
            yield line

    def _merge_includes(self, includes):
        for include in includes:
            in_includes = False
            for incl in self.includes:
                if include.module_name == incl.module_name:
                    in_includes = True
            if not in_includes:
                self.includes.append(include)

    def _merge_func_signs(self, func_signs):
        for func_sign in func_signs:
            self.func_signs.append(func_sign)

    def _merge_rest_code(self, rest_code):
        for code_stmt in rest_code:
            self.rest_code.append(code_stmt)

    def merge(self, generated):
        self._merge_includes(generated.includes)
        self._merge_func_signs(generated.func_signs)
        self._merge_rest_code(generated.rest_code)


class NodeGenerator(_layers.Layer):

    @_layers.register(objects.Val)
    def _val(self, val):
        if isinstance(val.type_, tuple(map(type, (
                objects.CTypes.int_fast8, objects.CTypes.int_fast32,
                objects.CTypes.int_fast64, objects.CTypes.uint_fast8,
                objects.CTypes.uint_fast32, objects.CTypes.uint_fast64)))):
            return val.literal
        elif isinstance(val.type_, type(objects.CTypes.char)):
            return "'" + val.literal + "'"
        errors.not_implemented()

    @_layers.register(objects.Var)
    def _var(self, var):
        return var.name

    def generate(self, node):
        result = Generated()
        # Append must depend on node's type.
        result.rest_code.append(self.get_registry()[node](node))
        return result


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
