from __future__ import annotations

import ast
import functools
import inspect
import json
import sys
from collections import OrderedDict
from fnmatch import fnmatch
from pathlib import Path
from typing import Callable
from typing import Container
from typing import Iterable
from typing import Sequence
from typing import Union

from docopt import DocoptLanguageError
from docopt import ParsedOptions
from docopt import docopt


__all__ = [
    "detect_args",
    "docopt_arguments",
    "docopt_main",
    "docopt_parse_docstrings",
    "make_conversion",
    "register_conversion",
]


def _try_convert(
    value: str,
    conversions: Iterable[Callable] = (int, float, complex, json.loads),
):
    """
    Try to apply the given conversion functions to the given
    string and return the result of whichever works first, if any.
    Conversion functions must raise :py:class:`ValueError` if the conversion fails.
    """
    for conversion in conversions:
        try:
            return conversion(value)
        except ValueError:
            pass
    return value


def make_conversion(pattern: str, func: Callable):
    """
    Create a function that applies the given conversion function
    to arguments whose names match the given pattern.

    Parameters:
        pattern: A :py:func:`fnmatch.fnmatch` pattern
        func: A function that accepts one string argument
            and returns the converted result
    """
    def conversion(name, value):
        if fnmatch(name, pattern):
            return func(value), True
        return value, False
    conversion.__doc__ = \
        f"Convert arguments with names matching {pattern} " \
        f"with function {func.__name__}."
    return conversion


class _Converter:
    conversions = OrderedDict([
        ("int", make_conversion("*int", int)),
        ("float", make_conversion("*float", float)),
        ("complex", make_conversion("*complex", complex)),
        ("path", make_conversion("*path", Path)),
        ("json", make_conversion("*json", json.loads)),
        ("str", make_conversion("*str", str)),
    ])

    @classmethod
    def register(cls, name, func):
        cls.conversions[name] = func

    @classmethod
    def convert(cls, name, value):
        if not isinstance(value, str):
            return value
        if isinstance(value, list):
            return [cls.convert(name, v) for v in value]
        for conversion in cls.conversions.values():
            value, ok = conversion(name, value)
            if ok:
                return value
        return _try_convert(value)


def register_conversion(name: str, func: Callable):
    """
    Register a function for automatic argument conversion.
    Functions must have signature
    :python:`conversion(name: str, value: str) -> Tuple[object, bool]`.
    If the conversion
    """
    _Converter.register(name, func)


def convert_argument(name: str, value: str) -> object:
    """
    If the given value is type :py:func:`str`, try to apply all registered
    argument conversions in order.
    If no conversion works the original string is returned.

    By default conversions are attempted as follows:
        - ``name`` matches ``*int`` → :py:class:`int`
        - ``name`` matches ``*float`` → :py:class:`float`
        - ``name`` matches ``*complex`` → :py:class:`complex`
        - ``name`` matches ``*path`` → :py:class:`pathlib.Path`
        - ``name`` matches ``*json`` → :py:func:`json.loads`
        - ``name`` matches ``*str`` → :py:class:`str`
        - try :py:class:`int`
        - try :py:class:`float`
        - try :py:class:`complex`
        - try :py:func:`json.loads`

    You can register new conversions (or replace existing ones)
    with :py:func:`register_conversion`.
    The final trial and error stage is fixed.
    """
    return _Converter.convert(name, value)


def convert_arguments(args: dict, simplify_names=True) -> Union[ParsedOptions, None]:
    """
    Apply :py:func:`convert_argument` to all argument values in
    the given dictionary.
    Returns a new :py:class:`docopt.ParsedOptions` dictionary with
    converted arguments, or None if input was None.

    If ``simplify_names`` is True argument names are simplified.
    Leading dashes are stripped, any remaining dashes are replaced
    with underscores, and angle brackets are removed.
    """
    if args is None:
        return None
    if simplify_names:
        def _name(name):
            return name.lstrip("-").replace("-", "_").replace("<", "").replace(">", "")
    else:
        def _name(name):
            return name
    return ParsedOptions(
        (_name(name), convert_argument(name, value))
        for name, value in args.items()
    )


def docopt_parse_docstrings(
    docstrings: Iterable[str],
    simplify_names=True,
    **kwargs,
) -> ParsedOptions:
    """
    Use the :py:func:`docopt` package to parse arguments based on the
    POSIX definition of calling syntax in the given docstrings.
    Arguments of the first successful parsing are returned.
    Raises ValueError if parsing all given docstrings fails.

    Arguments are converted from strings using :py:func:`convert_arguments`.

    Parameters:
        docstrings: docstrings to parse, None values are ignored
        simplify_names: if True, simplify argument names;
            See :py:func:`convert_arguments` for details
        kwargs: extra arguments passed to
            `docopt.docopt() <https://github.com/jazzband/docopt-ng#api>`_
    """
    parsed_args = None
    errors = []
    for s in docstrings:
        if s is None:
            continue
        try:
            parsed_args = docopt(s, **kwargs)
            break
        except DocoptLanguageError as e:
            errors.append(e)
            parsed_args = None
    if parsed_args is None:
        if errors:
            # backslashes are not allowed in f-string expressions...
            lines = "\n".join(map(str, errors))
            raise ValueError(
                "no valid docstrings found; "
                f"the following errors occurred: \n{lines}"
            )
        raise ValueError("no valid docstrings found")
    return convert_arguments(parsed_args, simplify_names=simplify_names)


def _is_main_module(f):
    module = inspect.getmodule(f)
    return module.__name__ == "__main__"


def docopt_arguments(f=None, main=False, main_guard=True, **kwargs):
    """
    Decorator to parse command line arguments using docopt.
    The decorated function must accept one positional argument, e.g.::

        @docopt_arguments
        def main(args):
            ...

    The function docstring is parsed first, then the module docstring.
    The first set of successfully parsed arguments is passed to the function.
    ValueError is raised if parsing fails for all docstrings.

    You can provide additional arguments, or override command line arguments
    by passing a dictionary to the wrapped function:
    :python:`main({"good": True})`.
    An empty dictionary (:python:`main({})`) has no effect.

    Parameters:
        f: the decorated function, filled in by the Python
        main: if True, immediately run ``f`` with parsed args
        main_guard: if True, guard execution of ``f`` with
            :python:`if __name__ == "__main__"`
        kwargs: extra arguments passed to
            `docopt.docopt() <https://github.com/jazzband/docopt-ng#api>`_
    """
    if f is None:
        return functools.partial(
            docopt_arguments,
            main=main,
            main_guard=main_guard,
            **kwargs,
        )
    module = inspect.getmodule(f)
    docstrings = [inspect.getdoc(f), inspect.getdoc(module)]
    parsed_args = docopt_parse_docstrings(docstrings, **kwargs)
    if main and (not main_guard or _is_main_module(f)):
        f(parsed_args)
    @functools.wraps(f)
    def wrapper(args):
        if isinstance(args, dict):
            args = ParsedOptions(parsed_args, **args)
        else:
            args = parsed_args
        f(args)
    return wrapper


def docopt_main(f=None, main_guard=True, **kwargs):
    """
    Decorator to parse command line arguments using
    `docopt <https://github.com/jazzband/docopt-ng>`.
    This is an alias for::

        @docopt_arguments(main=True)
        def main(args):
            ...

    Functions decorated like this are immediately executed,
    so they need to be located at the end of the file after
    any other definitons.
    If this is not what you want,
    use :py:func:`docopt_arguments` instead::

        @docopt_arguments
        def main(args):
            ...
        
        if __name__ == "__main__":
            main({})
    """
    return docopt_arguments(f=f, main=True, main_guard=main_guard, **kwargs)


def _decorator_name(decorator: ast.AST):
    """
    Find the function name of a decorator in an :py:class:`ast.AST` node.
    """
    while decorator:
        name = getattr(decorator, "attr", None) or getattr(decorator, "id", None)
        if name:
            return name
        decorator = getattr(decorator, "func", None)
    return None


DOCOPT_DECORATORS = "docopt_arguments", "docopt_main"


def _find_docstrings_code(
    code: str,
    decorators: Container[str] = DOCOPT_DECORATORS,
) -> Sequence[Union[str, None]]:
    """
    Parse the given Python code and return the docstrings of
    all functions decorated with the given decorator function names,
    as well as the docstring of the module, if any.

    Parameters:
        code: Python code to parse
        decorators: list of decorator names that are included,
            defaults to ("docopt_arguments", "docopt_main")
    """
    tree = ast.parse(code)
    docstrings = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for decorator in getattr(node, "decorator_list", ()):
                if _decorator_name(decorator) in decorators:
                    docstrings.append(ast.get_docstring(node))
    docstrings.append(ast.get_docstring(tree))
    return docstrings


def _find_docstrings_path(
    path: Union[str, Path],
    decorators: Container[str] = DOCOPT_DECORATORS,
) -> Sequence[Union[str, None]]:
    """
    Parse the file at path and extract all relevant docstrings.
    See :py:func:`_find_docstrings_code` for details.
    """
    with open(path, encoding='utf-8') as fp:
        return _find_docstrings_code(fp.read(), decorators=decorators)


def detect_args(path: Union[Path, str, None] = None, **kwargs) -> Union[ParsedOptions, None]:
    """
    Try to detect command line arguments using docopt.
    Docstrings are extracted from the file at the given path.
    :python:`sys.argv[0]` is used if no path is given.

    First, docstrings of functions decorated with :py:func:`docopt_arguments`
    or :py:func:`docopt_main` are parsed in the order that they appear,
    and finally the module docstring.
    The first set of arguments that is successfully parsed is returned.

    Parameters:
        path: Use docstrings from this file, or :python:`sys.argv[0]` if None
        kwargs: extra arguments passed to
            `docopt.docopt() <https://github.com/jazzband/docopt-ng#api>`_
    """
    docstrings = _find_docstrings_path(path or sys.argv[0])
    return docopt_parse_docstrings(docstrings, **kwargs)
