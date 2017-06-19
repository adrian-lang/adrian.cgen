from . import errors
from . import objects
from . import _context
from . import _layers


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
        return self.get_registry()[node](node)
