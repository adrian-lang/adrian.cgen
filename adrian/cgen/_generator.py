from . import errors
from . import objects
from . import _context
from . import _layers


_CTYPE_TO_STRING = {
    key: value + "_t"
    for key, value in [
        (type(ctype), val)
        for ctype, val in [
            (objects.CTypes.int_fast8, "int_fast8"),
            (objects.CTypes.int_fast32, "int_fast32"),
            (objects.CTypes.int_fast64, "int_fast64"),
            (objects.CTypes.uint_fast8, "uint_fast8"),
            (objects.CTypes.uint_fast32, "uint_fast32"),
            (objects.CTypes.uint_fast64, "uint_fast64")
        ]]
}


class Generated:

    def __init__(self, includes=None, func_signs=None, rest_code=None):
        self.includes = includes or []
        self.func_signs = func_signs or []
        self.rest_code = rest_code or []

    def to_csource(self):
        general_list = self.includes + self.func_signs + self.rest_code
        for line in general_list:
            yield line

    def _merge_includes(self, includes):
        for include in includes:
            if include not in self.includes:
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
    _includes = []

    def add_include_string(self, include_string):
        if include_string not in self._includes:
            self._includes.append(include_string)

    def add_include(self, include):
        include_string = " ".join(["#include", include])
        self.add_include_string(include_string)

    def type_(self, type_):
        # TODO: support other types.
        if isinstance(type_, tuple(map(type, (
                objects.CTypes.int_fast8, objects.CTypes.int_fast32,
                objects.CTypes.int_fast64, objects.CTypes.uint_fast8,
                objects.CTypes.uint_fast32, objects.CTypes.uint_fast64)))):
            self.add_include("<stdint.h>")
            return _CTYPE_TO_STRING[type(type_)]
        errors.not_implemented("type is not supported")

    def sub_decl(self, decl):
        """Generates declaration without semicolon."""
        # TODO: support decl.expr.
        return " ".join([
            self.type_(decl.type_),
            decl.name
        ])

    @_layers.register(objects.Decl)
    def decl(self, decl):
        """Generates declaration with semicolon."""
        return "".join([self.sub_decl(decl), ";"])

    @_layers.register(objects.Struct)
    def struct(self, struct_decl):
        # Generating body.
        generated_body = Generated()
        for stmt in struct_decl.body:
            generated_body.merge(self.generate(stmt))

        # Updating includes.
        for include in generated_body.includes:
            self.add_include_string(include)

        body = "{\n" + "\n".join(generated_body.rest_code) + "\n}"
        return " ".join([
            "struct",
            struct_decl.name,
            "".join([body, ";"])
        ])

    def generate(self, node):
        node_result = self.get_registry()[node](node)
        return Generated(
            includes=self._includes, rest_code=[node_result])
