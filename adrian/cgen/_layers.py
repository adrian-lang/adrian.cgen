import types
import functools

from paka import funcreg


_PREREGISTERED_NODE_CLASSES_ATTR_NAME = "_layer_prereg_nodes_clss"
_INTERNAL_REGISTRY_ATTR_NAME = "_registry"


def register(*node_classes):
    def _wrapper(func):
        setattr(func, _PREREGISTERED_NODE_CLASSES_ATTR_NAME, node_classes)
        return func
    return _wrapper


class LayerMeta(type):

    def __new__(cls, name, bases, attrs):
        # Layer does not have bases, so we filter it out this way.
        if bases:
            registry = funcreg.TypeRegistry()
            for value in attrs.values():
                if isinstance(value, types.FunctionType):
                    for node_class in getattr(
                            value, _PREREGISTERED_NODE_CLASSES_ATTR_NAME, ()):
                        registry.register(value, node_class)
            attrs[_INTERNAL_REGISTRY_ATTR_NAME] = registry
        return type.__new__(cls, name, bases, attrs)


class Layer(metaclass=LayerMeta):

    def __init__(self):
        pass

    def get_registry(self):
        reg = funcreg.TypeRegistry()
        for node_class, func in getattr(
                self, _INTERNAL_REGISTRY_ATTR_NAME).items():
            reg.register(functools.partial(func, self), node_class)
        return reg
