class _Namespace:

    def __init__(self):
        self._scope = 0
        self._space = {self._scope: {}}

    def add_name(self, name, value):
        self._space[self._scope][name] = value

    def del_name(self, name):
        del self._space[self._scope][name]

    def add_scope(self):
        self._scope += 1
        self._space[self._scope] = {}

    def del_scope(self):
        self._scope -= 1
        del self._space[self._scope]

    def exists(self, name):
        return name in self._space[self._scope]

    def get(self, name):
        if self.exists(name):
            return self._space[self._scope][name]
        return None

    @property
    def scope(self):
        return self._scope


class Context:

    def __init__(self):
        self.namespace = _Namespace()
        self.typespace = _Namespace()
        self.funcspace = _Namespace()
