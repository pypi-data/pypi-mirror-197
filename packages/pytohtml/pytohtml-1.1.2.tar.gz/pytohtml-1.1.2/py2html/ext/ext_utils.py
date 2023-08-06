import time
import typing as _t

from strbuilder import Builder
from flask import Flask

T = _t.TypeVar('T')


def cache(func: _t.Callable[[], T]) -> T:
    if not hasattr(func, '__cached__'):
        func.__cached__ = func()
    return func.__cached__


T = _t.TypeVar('T', bound=_t.Callable)


def api(app: Flask, rule: str, json: bool=True, **options: _t.Any) -> str:
    def decorator(func: T) -> T:
        app.route(rule=rule, **options)(func)
        return Builder(f'''const {func.__name__} = async (data = {{}}) => {{return (await fetch(`{rule}`, {{
                    method: 'POST',
                    mode: 'cors',
                    cache: 'no-cache',
                    credentials: 'same-origin',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    redirect: 'follow',
                    referrerPolicy: 'no-referrer',
                    body: JSON.stringify(data)
            }}))''').write_if(json, '.json()').write('}').build().replace('    ', '')
    return decorator


time_names = {
    1: 'ns',
    1000000: 'ms',
    1000: 'second',
    60: 'minute',
    60: 'hour',
    24: 'day',
    356: 'year'
}


def format_time_ns(time) -> str:
    """
    :test
    a = 1
    while True:
        print(format_time_ns(a))
        a *= 2
        time.sleep(0.1)
    """
    last = 'ns'
    for order, name in time_names.items():
        if time / order < 1:
            break
        time /= order
        last = name
    return f'{time:0.2f}{last}'


def timer(func: T = None, log_callback: _t.Callable[[str], _t.Any] = print):
    def decorator(func: T) -> T:
        def wrapper(*args, **kwargs):
            start_time = time.time_ns()
            result = func(*args, **kwargs)
            end_time = time.time_ns()
            log_callback(format_time_ns(end_time-start_time))
            return result
        return wrapper

    if func is None:
        return decorator

    return decorator(func)
