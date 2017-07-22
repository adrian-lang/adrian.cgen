from . import errors
from . import objects
from . import _context
from . import _layers


_CTYPE_TO_STRING = {
    key: value
    for key, value in [
        (type(ctype), val)
        for ctype, val in [
            (objects.CTypes.int_fast8, "int_fast8_t"),
            (objects.CTypes.int_fast32, "int_fast32_t"),
            (objects.CTypes.int_fast64, "int_fast64_t"),
            (objects.CTypes.uint_fast8, "uint_fast8_t"),
            (objects.CTypes.uint_fast32, "uint_fast32_t"),
            (objects.CTypes.uint_fast64, "uint_fast64_t"),
            (objects.CTypes.int, "int"),
            (objects.CTypes.void, "void"),
            (objects.CTypes.char, "char"),
        ]]
}


_COP_TO_STRING = {
    key: value
    for key, value in [
        (type(cop), val)
        for cop, val in [
            (objects.COps.plus, "+"),
            (objects.COps.minus, "-"),
            (objects.COps.star, "*"),
            (objects.COps.slash, "/"),
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
        for include in sorted(includes):
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

    def __init__(self):
        self._includes = []

    def add_include_string(self, include_string):
        if include_string not in self._includes:
            self._includes.append(include_string)

    def add_include(self, include):
        self.add_include_string(
            "#include <{}>".format(include.module_name))

    def type_(self, type_):
        # TODO: support other types.
        if isinstance(type_, tuple(map(type, (
                objects.CTypes.int_fast8, objects.CTypes.int_fast32,
                objects.CTypes.int_fast64, objects.CTypes.uint_fast8,
                objects.CTypes.uint_fast32, objects.CTypes.uint_fast64)))):
            self.add_include(objects.Include("stdint.h"))
            return _CTYPE_TO_STRING[type(type_)]
        elif isinstance(type_, (objects._Void, objects._Int)):
            return _CTYPE_TO_STRING[type(type_)]
        elif isinstance(type_, objects.StructType):
            return "struct {}".format(type_.name)
        elif isinstance(type_, objects._Ptr):
            # Recursively call self.type_ with ptr's "inner" type.
            return "{}*".format(self.type_(type_.type_))
        elif isinstance(type_, objects._Array):
            # Recursively call self.type_ with array's "inner" type.
            return self.type_(type_.type_)
        errors.not_implemented("type is not supported")

    def expr(self, expr):
        if isinstance(expr, objects.FuncCall):
            return self.sub_func_call(expr)
        elif isinstance(expr, objects.SizeOf):
            return "sizeof({})".format(self.type_(expr.type_))
        elif isinstance(expr, objects.Expr):
            return self.sub_sexpr(expr)
        elif isinstance(expr, objects.Var):
            return self.sub_var(expr)
        elif isinstance(expr, objects.Val):
            return self.sub_val(expr)
        elif isinstance(expr, objects.ArrayElemByIndex):
            return self.sub_array_elem_by_index(expr)
        #elif isinstance(expr, objects._Ptr):
        #    return "*{}".format(self.expr(expr.type_))
        elif isinstance(expr, objects.StructElem):
            if isinstance(expr.struct_name, objects._Ptr):
                sep = "->"
                struct_name = self.expr(expr.struct_name.type_)
            else:
                sep = "."
                struct_name = self.expr(expr.struct_name)
            return "{}{}{}".format(struct_name, sep, self.expr(expr.elem_name))
        errors.not_implemented("expr is not supported")

    def sub_decl(self, decl):
        """Generates declaration without semicolon."""
        # For example, in
        # struct MyStruct* self = malloc(sizeof(struct MyStruct))
        # result is: struct MyStruct* self
        # decl.expr is: malloc(sizeof(struct MyStruct))
        result = "{} {}".format(self.type_(decl.type_), decl.name)
        # If it is an array, add size of array (or at least square brackets).
        if isinstance(decl.type_, objects._Array):
            orig_size = decl.type_.size
            if orig_size is None:
                size = ""
            elif isinstance(orig_size, int):
                size = str(orig_size)
            elif orig_size == "auto":
                size = str(len(decl.expr.literal))
            result = "".join([result, "[", size, "]"])
        if decl.expr:
            result = " ".join([result, "=", self.expr(decl.expr)])
        return result

    def args(self, args):
        if isinstance(args, objects._Void):  # 0 arguments
            return ["void"]
        return [self.sub_decl(arg) for arg in args]

    def sub_func_call(self, call):
        # Updating includes.
        for include in call.includes:
            self.add_include(include)
        return "{}({})".format(call.name, ", ".join(map(self.expr, call.args)))

    def sub_array_elem_by_index(self, expr):
        return "{}[{}]".format(expr.name, self.expr(expr.index))

    @_layers.register(objects.ArrayElemByIndex)
    def array_elem_by_index(self, expr):
        return "".join([self.sub_array_elem_by_index(expr), ";"])

    def sub_sexpr(self, expr):
        return "{} {} {}".format(
            self.expr(expr.expr1), _COP_TO_STRING[type(expr.op)],
            self.expr(expr.expr2))

    @_layers.register(objects.Expr)
    def sexpr(self, expr):
        return "".join([self.sub_sexpr(expr), ";"])

    def sub_var(self, variable):
        return variable.name

    @_layers.register(objects.Var)
    def var(self, variable):
        return "".join([self.sub_var(variable), ";"])

    def sub_val(self, value):
        if isinstance(value.type_, tuple(map(type, (
                objects.CTypes.int_fast8, objects.CTypes.int_fast32,
                objects.CTypes.int_fast64, objects.CTypes.uint_fast8,
                objects.CTypes.uint_fast32, objects.CTypes.uint_fast64)))):
            self.add_include(objects.Include("stdint.h"))
            return value.literal
        elif isinstance(value.type_, (objects._Int, objects._SizeT)):
            return str(value.literal)
        elif isinstance(value.type_, objects._Char):
            return "'{}'".format(value.literal)
        elif isinstance(value.type_, objects._Ptr):
            ptr = value.type_
            if isinstance(ptr.type_, objects._Char):
                return '"{}"'.format(value.literal)
        elif isinstance(value.type_, objects._Array):
            return "{{{}}}".format(
                ", ".join([self.expr(subexpr) for subexpr in value.literal]))
        errors.not_implemented("val is not supported")

    @_layers.register(objects.Val)
    def val(self, value):
        return "".join([self.sub_val(value), ";"])

    @_layers.register(objects.FuncCall)
    def func_call(self, call):
        return "{};".format(self.sub_func_call(call))

    @_layers.register(objects.Decl)
    def decl(self, decl):
        """Generates declaration with semicolon."""
        return "".join([self.sub_decl(decl), ";"])

    @_layers.register(objects.Assignment)
    def assignment(self, assmt):
        # Currently we use self.expr, as assmt.name can be expression,
        # e.g. self->data.
        name = self.expr(assmt.name)
        expr = self.expr(assmt.expr)
        return "{} = {};".format(name, expr)

    @_layers.register(objects.Struct)
    def struct_decl(self, struct):
        # Generating body.
        generated_body = Generated()
        for stmt in struct.body:
            generated_body.merge(self.generate(stmt))

        # Updating includes.
        for include in generated_body.includes:
            self.add_include_string(include)

        body = "{\n" + "\n".join(generated_body.rest_code) + "\n}"
        return " ".join([
            "struct",
            struct.name,
            "".join([body, ";"])
        ])

    @_layers.register(objects.Func)
    def func_decl(self, func):
        # Generating body.
        generated_body = Generated()
        for stmt in func.body:
            generated_body.merge(self.generate(stmt))

        # Updating includes.
        for include in generated_body.includes:
            self.add_include_string(include)

        rettype = self.type_(func.rettype)
        args = self.args(func.args)

        return " ".join([
            rettype,
            "".join([func.name, "(", ", ".join(args), ")"]),
            "{\n" + "\n".join(generated_body.rest_code) + "\n}"
        ])

    @_layers.register(objects.Return)
    def return_(self, return_):
        return "return {};".format(self.expr(return_.expr))

    def generate(self, node):
        node_result = self.get_registry()[node](node)
        return Generated(
            includes=self._includes, rest_code=[node_result])
