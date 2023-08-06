import typing as t
import html
import py2xml

T = t.TypeVar('T')
V = t.TypeVar('V')

P = t.ParamSpec('P')

Boolean = {True: 'true', False: 'false'}

Value = t.List | t.Text | bool


def format(x: Value) -> str:
    if isinstance(x, str):
        return x
    if isinstance(x, bool):
        return Boolean[x]

    try:
        return ' '.join(x)
    except:
        return str(x)


class HTMLElement(t.Generic[P], py2xml.Element[P]):

    def __call__(self, *args: P.args, **props: P.kwargs) -> t.Self:
        attributes = {}
        if 'htmlFor' in props:
            attributes['for'] = props.pop('htmlFor')
        if 'className' in props:
            attributes['class'] = props.pop('className')
        return super().__call__(*args, **props, **attributes) # type: ignore

    def render(self) -> str:
        children_text = self.children_text

        return f'<{self.name}%s>%s</{self.name}>' % (
            ' %s' % ' '.join(
                '%s="%s"' % (k, format(v)) if v is not None else k for k, v in self.attributes.items()
            ) if self.attributes else '',
            '%s' % children_text if children_text else '',
        )


def from_name(
    name: str,
    *,
    attrs: t.Callable[P, None] = None,
    children: t.Optional[t.List['Value']] = None,
    props: t.Optional[t.Dict[t.Text, t.Optional[t.Any]]] = None
) -> HTMLElement[P]:
    ...


from_name = HTMLElement.from_name # type: ignore
