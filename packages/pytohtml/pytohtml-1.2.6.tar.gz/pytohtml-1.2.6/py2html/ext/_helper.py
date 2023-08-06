import typing as t

T = t.TypeVar('T')

def instance(clazz: t.Callable[[], T]) -> T:
    return clazz()