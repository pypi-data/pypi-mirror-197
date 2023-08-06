from typing import Callable, Dict, List
from py2html import HTMLElement
import random, string

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

class Styler:
    def __init__(self, keys: List[str]) -> None:
        self.keys = keys

    def __call__(self, element: HTMLElement) -> HTMLElement:
        element.attributes['class'] = ' '.join(self.keys)
        return element

    def __or__(self, other: 'Styler') -> 'Styler':
        return Styler(self.keys + other.keys)


class Style(HTMLElement):
    def __init__(self):
        self.styles = {}
        self.variables = {}

    def __call__(self, style: Dict[str, str]) -> Callable[[HTMLElement], HTMLElement]:
        key = random_string(4)
        self.styles[f'.{key}'] = ';'.join(f'{k}:{v}' for k, v in style.items())

        return Styler([key])

    def style(self, target: str, style: Dict[str, str]) -> None:
        self.styles[target] = ';'.join(f'{k}:{v}' for k, v in style.items())

    def define(self, value: str) -> str:
        key = f'--{random_string(4)}'
        self.variables[key] = value
        return f'var({key})'

    def render(self) -> str:
        self.styles[':root'] = ';'.join(f'{k}:{v}' for k, v in self.variables.items())
        return '<style>%s</style>' % ''.join(f'{k} {{{v}}}' for k, v in self.styles.items())