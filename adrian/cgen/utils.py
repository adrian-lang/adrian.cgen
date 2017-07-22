from adrian.cgen import Func, CTypes


def make_main0(*body):
    """Make 0-argument main: int main(void) {...}."""
    return Func(
        "main", rettype=CTypes.int,
        args=CTypes.void, body=body)
