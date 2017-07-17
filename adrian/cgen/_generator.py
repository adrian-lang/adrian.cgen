from . import errors
from . import objects
from . import _context
from . import _layers


_CTYPES_TO_STRINGS = {
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
            in_includes = False
            for incl in self.includes:
                if include == incl:
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
    _includes = []

    def _subadd_include(self, include):
        if include not in self._includes:
            self._includes.append(include)

    def _add_include(self, include):
        include_string = " ".join([
            "#include",
            include])
        self._subadd_include(include_string)

    def _type(self, type_):
        # TODO: only int types are supported.
        self._add_include("<stdint.h>")
        return _CTYPES_TO_STRINGS[type(type_)]

    def _expr(self, expr):
        if isinstance(expr, objects.Val):
            return self._val(expr)
        elif isinstance(expr, objects.Var):
            return self._var(expr)
        errors.not_implemented()

    def _sub_decl(self, decl):
        """Generates decl without semicolon."""
        result = " ".join([
            self._type(decl.type_),
            decl.name
        ])
        if not decl.expr is None:
            result += " ".join(["", "=", self._expr(decl.expr)])
        return result

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

    @_layers.register(objects.Decl)
    def _decl(self, decl):
        """Generates decl with semicolon."""
        return "".join([self._sub_decl(decl), ";"])

    def _func_decl_args(self, args):
        result = []
        for arg in args:
            result.append(self._sub_decl(arg))
        return result

    @_layers.register(objects.Func)
    def _func_decl(self, func_decl):
        # HARDCORE! FIXME!
        rettype = self._type(func_decl.rettype)
        generated_body = Generated()
        for stmt in func_decl.body:
            generated_body.merge(self.generate(stmt))
        for include in generated_body.includes:
            self._subadd_include(include)
        name = func_decl.name
        args = "(" + ", ".join(self._func_decl_args(func_decl.args)) + ")"
        body = "{\n" + "\n  ".join([""] + generated_body.rest_code) + "\n}"
        return " ".join([rettype, name, args, body])

    @_layers.register(objects.Return)
    def _return_stmt(self, return_stmt):
        return "".join(["return", " ", self._expr(return_stmt.expr), ";"])

    def generate(self, node):
        # TODO: Only one stmt is supported.
        node_result = self.get_registry()[node](node)
        return Generated(
            includes=self._includes, rest_code=[node_result])
