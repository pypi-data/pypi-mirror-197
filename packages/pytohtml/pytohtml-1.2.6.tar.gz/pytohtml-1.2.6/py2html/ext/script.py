from typing import Callable, Generic, ParamSpec, Self

import py2js

from py2html import HTMLElement

P = ParamSpec('P')


class ScriptHandle(Generic[P]):
    def __init__(self, func_name: str) -> None:
        self.func_name = func_name

    def __call__(self, *args: P.args, **props: P.kwargs) -> Self:
        parts = []
        if args:
            parts.extend(map(str, args))
        if props:
            parts.append('{%s}' % ','.join('%s: %s' % (k, format(v)) if v is not None else k for k, v in props.items()))

        return f'{self.func_name}({", ".join(parts)})'

    def __str__(self) -> str:
        return f'{self.func_name}()'


class Script(HTMLElement):
    def __init__(self) -> None:
        super().__init__('script')
        self.on_loaded = []

    def __call__(self, func: Callable) -> str:
        self.children.append(py2js.js(func, as_function=True))
        return ScriptHandle(func.__name__)

    def on(self, id: str, event: str) -> Callable[[Callable], None]:
        def decorator(func: Callable) -> str:
            self.children.append(py2js.js(func, as_function=True))
            self.on_loaded.append(f'document.getElementById("{id}").addEventListener("{event}", {func.__name__})')
        return decorator

    def render(self) -> str:
        scripts = []
        if self.children:
            scripts.append('\n'.join(map(str, self.children)))
        if self.on_loaded:
            scripts.append('document.addEventListener("DOMContentLoaded", () => {%s})' % '\n'.join(self.on_loaded))
        return '<script>%s</script>' % '\n'.join(scripts)
