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


class NodeGenerator(_layers.Layer):
    _includes = []

    def _add_include(self, include):
        include_string = " ".join([
            "#include",
            include])
        if include_string not in self._includes:
            self._includes.append(include_string)

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
        return " ".join([
            self._type(decl.type_),
            decl.name,
            "=",
            "".join([self._expr(decl.expr), ";"])
        ])

    def generate(self, node):
        # TODO: Only one stmt is supported.
        if self._includes:
            return "\n\n".join([
                "\n".join(self._includes),
                self.get_registry()[node](node)
            ])
        return self.get_registry()[node](node)
