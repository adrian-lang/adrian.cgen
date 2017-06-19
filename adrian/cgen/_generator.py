from . import errors
from . import objects
from . import _context
from . import _layers


class NodeGenerator(_layers.Layer):

    def _type(self, type_):
        # TODO: implement
        # return "int"
        errors.not_implemented()

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
        return self.get_registry()[node](node)
