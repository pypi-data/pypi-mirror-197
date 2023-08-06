import pathlib
import typing as t

from ._helper import instance
from py2xml import Element
from py2html import HTMLElement, elements
import sass


class Element(HTMLElement):
    def copy(self) -> t.Self:
        return type(self)()


class FileLink(Element):

    def set_attributes(self, attributes: t.Dict):
        if 'href' in attributes:
            self.children.append(pathlib.Path(attributes['href']).read_text())


@instance
class CSS(FileLink):

    def __init__(self) -> None:
        super().__init__('style')

    def render(self) -> str:
        return f'<style>{self.children_text}</style>'


@instance
class SASS(FileLink):

    def __init__(self) -> None:
        super().__init__('style')

    def render(self) -> str:
        return f'<style>{sass.compile(string=self.children_text)}</style>'


Link = elements.a


@instance
class Button(Element):
    def __init__(self) -> None:
        super().__init__('input', props={'type': 'submit'})
