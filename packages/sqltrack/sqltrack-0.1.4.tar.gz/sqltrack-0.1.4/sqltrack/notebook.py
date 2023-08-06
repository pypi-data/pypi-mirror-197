from __future__ import annotations

import hashlib
import inspect
import math
from datetime import datetime
from datetime import timedelta
from functools import partial
from pathlib import Path
from typing import Sequence
from typing import Union

import humanize
from IPython.display import HTML
from IPython.display import display

import pandas as pd

__all__ = [
    "init_notebook_mode",
    "textcolor",
    "format_marked",
    "format_status",
    "format_tags",
    "format_datetime",
    "format_datetime_relative",
    "format_timedelta",
    "format_percentage",
    "format_float",
    "format_dataframe",
]


def _isnan(v):
    try:
        return math.isnan(v)
    except TypeError:
        return False


def _not_a_value(v):
    return v is None or _isnan(v) or pd.isnull(v)


CSS_DIR = (Path(__file__).parent / "css").absolute()


def init_notebook_mode():
    """
    Add the sqltrack stylesheet to the notebook.
    """
    path = CSS_DIR / "notebook.css"
    with path.open() as fp:
        display(HTML("<style>\n" + fp.read() + "\n</style>"))


COLORS = [
    'Amethyst', 'Blue', 'Caramel', 'Damson', 'Ebony', 'Forest', 'Green',
    'Honeydew', 'Iron', 'Jade', 'Khaki', 'Lime', 'Mallow', 'Navy',
    'Orpiment', 'Pink', 'Quagmire', 'Red', 'Sky', 'Turquoise', 'Uranium',
    'Violet', 'Wine', 'Xanthin', 'Yellow', 'Zinnia',
]


def textcolor(text: str, colors: Sequence[str] = None):
    """
    Return a color name for the given text, based on its hash value.
    """
    if colors is None:
        colors = COLORS
    h = hashlib.blake2b(text.encode('utf-8'), digest_size=1).digest()
    return colors[int.from_bytes(h, byteorder='big') % len(colors)]


def format_marked(is_marked: bool):
    """
    If ``is_marked`` is True, return a gold star, else empty string.
    """
    if is_marked:
        return '<span class="invisible">marked</span>' \
            + '<span title="marked" class="marked">⭐</span>'
    return ''


def format_status(status: str):
    """
    Return an icon for the given status.
    """
    return f'<span class="invisible">{status}</span>' \
        + f'<span title="{status}" class="status {status}"></span>'


def format_tags(tags: dict):
    """
    Return tag bubbles for the given tags.
    """
    tags = tags or {}
    tags.pop("marked", None)
    return " ".join(f'<span title="{t}" class="tag {textcolor(t)}">{t}</span>' for t in tags)


def format_bool(b: bool, na_rep="--") -> str:
    """
    Return bool value.

    Parameters:
        b: bool to format
        na_rep: replacement string for NaN values
    """
    rep = b
    if b is None:
        rep = na_rep
    elif b:
        rep = "⏺"
    else:
        rep = "⭘"
    return f'<span title="{b}" class="center">{rep}</span>'


def format_string(s: str, ellipsis="left", na_rep="--") -> str:
    """
    Return string wrapped to display long text with ellipsis.

    Parameters:
        s: string to wrap
        ellipsis: if "left" (default), ellipsis is placed on the
            left and the end is displayed fully;
            if True, ellipsis is placed on the right and the
            beginning of the string is displayed;
            if False, the string is returne as-is
        na_rep: replacement string for NaN values
    """
    rep = s
    if s is None:
        rep = na_rep
    if ellipsis == "left":
        return f'<span class="ellipsis-left"><bdi title="{s}">{rep}</bdi></span>'
    if ellipsis:
        return f'<span class="ellipsis-right" title="{s}">{rep}</span>'
    return s


def _localize(dt: datetime):
    try:
        # unlike native datetime objects, pandas timestamps simply
        # drop the timezone when astimezone is called with tz=None,
        # so we try to convert to native datetime first...
        dt = dt.to_pydatetime(warn=False)
    except TypeError:
        pass
    return dt.astimezone().replace(tzinfo=None)


def format_datetime(dt: datetime, sep=" ", timespec="seconds", na_rep="--") -> str:
    """
    Return datetime in ISO format.

    Parameters:
        dt: datetime to format
        sep: date and time separator
        timespec: precision of the time part, one of 'auto', 'hours',
            'minutes', 'seconds', 'milliseconds' and 'microseconds'
        na_rep: replacement string for NaN values
    """
    if _not_a_value(dt):
        return na_rep
    dt = _localize(dt)
    s = dt.isoformat(sep=sep, timespec=timespec)
    return f'<span class="invisible">{dt}</span><span>{s}</span>'


def format_datetime_relative(dt: datetime, sep=" ", timespec="seconds", na_rep="--") -> str:
    """
    Return time since given datetime in human-readable form.

    Parameters:
        dt: datetime to format
        sep: date and time separator
        timespec: precision of the time part, one of 'auto', 'hours',
            'minutes', 'seconds', 'milliseconds' and 'microseconds'
        na_rep: replacement string for NaN values
    """
    if _not_a_value(dt):
        return na_rep
    dt = _localize(dt)
    natural = humanize.naturaltime(dt)
    title = dt.isoformat(sep=sep, timespec=timespec)
    return f'<span class="invisible">{title}</span><span title="{title}">{natural}</span>'


def format_timedelta(td: timedelta, na_rep="--") -> str:
    """
    Return a timedelta in human-readable form.

    Parameters:
        td: timedelta to format
        na_rep: replacement string for NaN values
    """
    if _not_a_value(td):
        return na_rep
    seconds = td.total_seconds()
    if math.isnan(seconds):
        return na_rep
    natural = humanize.naturaldelta(td)
    title = str(timedelta(seconds=round(seconds)))
    return f'<span class="invisible">{title}</span><span title="{title}">{natural}</span>'


def format_percentage(v, mul=100, spec=".1f", na_rep="--") -> str:
    """
    Returns a percentage value with bar in background.

    Parameters:
        v: percentage value to format
        mul: multiplicative factor for display;
            defaults to 100 for float values in [0,1]
        spec: format spec; default :python:`".1f"`
        na_rep: replacement string for NaN values
    """
    if _not_a_value(v):
        return na_rep
    classes = "bar"
    sortvalue = v
    v *= mul
    pct = int(round(v))
    prop = f"padding-right: {mul-pct+5}%"
    if v < 50:
        classes += " left"
        prop = f"text-indent: {pct+5}%"
    return f'<span class="invisible">{sortvalue}</span>' \
        + f'<span class="{classes}" style="background: linear-gradient' \
        + f'(to right, var(--barcolor) {pct}%, transparent 0%); ' \
        + f'{prop}">{v:{spec}}%</span>'


def format_float(v: float, spec=".2f", na_rep="--") -> str:
    """
    Format a float value.

    Parameters:
        v: float value to format
        spec: format spec; default :python:`".2f"`
        na_rep: replacement string for NaN values
    """
    rep = v
    if _not_a_value(v):
        rep = na_rep
    else:
        rep = f"{v:{spec}}"
    return f"<span title={v}>{rep}</span>"


DEFAULT_MAPPING = {
    " ": format_marked,
    "m": format_marked,
    "marked": format_marked,
    "s": format_status,
    "status": format_status,
    "tags": format_tags,
    "progress": format_percentage,
}


def _is_datetime(v):
    return pd.api.types.is_datetime64_any_dtype(v)


def _is_timedelta(v):
    return pd.api.types.is_timedelta64_dtype(v)


def _is_float(v):
    return pd.api.types.is_float_dtype(v)


def _is_bool(v):
    return pd.api.types.is_bool_dtype(v)


def _is_string(v):
    return pd.api.types.is_string_dtype(v)


def _partial_function(func, **kwargs):
    parameters = inspect.signature(func).parameters
    mapped_kwargs = {k: v for k, v in kwargs.items() if k in parameters}
    return partial(func, **mapped_kwargs)


def _normalize(v):
    try:
        return v.lower()
    except AttributeError:
        return v


def format_dataframe(
    df: pd.DataFrame,
    formatting: Union[dict, None] = None,
    na_rep="--",
    relative_datetimes: bool = True,
    string_ellipsis: Union[str, bool] = "left",
) -> str:
    """
    Returns a copy of the given Pandas DataFrame with
    formatting applied.

    By default the following functions are applied to
    these the following columns (case-insensitive):

    * ``" "``: :py:func:`format_marked`
    * ``"m"``: :py:func:`format_marked`
    * ``"marked"``: :py:func:`format_marked`
    * ``"s"``: :py:func:`format_status`
    * ``"status"``: :py:func:`format_status`
    * ``"tags"``: :py:func:`format_tags`
    * ``"progress"``: :py:func:`format_percentage`

    If the column name is not found in the formatting
    function dictionary, then the formatting function
    is selected based based on dtype:

    * Any :py:class:`datetime`-like: :py:func:`format_datetime_relative`
      or :py:func:`format_datetime` if ``relative_datetimes`` is False
    * Any :py:class:`str`-like: :py:func:`format_string` with the given
      ``string_ellipsis`` parameter

    Parameters:
        formatting: overwrite the default format functions
            for named columns; names are case-insensitive
        relative_datetimes: if True (default), use
            :py:func:`format_datetime_relative` for columns with
            datetime-like dtype, else :py:func:`format_datetime`
        string_ellipsis: passed as ``ellipsis`` parameter to
            :py:func:`format_string` for columns with str-like dtype
    """
    formatting = dict(DEFAULT_MAPPING, **(formatting or {}))
    formatting = {
        _normalize(name): _partial_function(
            func,
            na_rep=na_rep,
            ellipsis=string_ellipsis,
        )
        for name, func in formatting.items()
    }
    # use a shallow copy of the DataFrame so we can replace columns
    df = df.copy(deep=False)
    # remember correct functions to call for types
    # so we don't have to do this for every column
    format_datetime_ = partial(format_datetime, na_rep=na_rep)
    if relative_datetimes:
        format_datetime_ = partial(format_datetime_relative, na_rep=na_rep)
    format_timedelta_ = partial(format_timedelta, na_rep=na_rep)
    format_string_ = partial(format_string, na_rep=na_rep, ellipsis=string_ellipsis)
    format_float_ = partial(format_float, na_rep=na_rep)
    format_bool_ = partial(format_bool, na_rep=na_rep)
    # apply formatting to columns
    for c in df.columns:
        col = df[c]
        func = formatting.get(_normalize(c))
        if func:
            df[c] = col.apply(func)
        elif _is_datetime(col):
            df[c] = col.apply(format_datetime_)
        elif _is_timedelta(col):
            df[c] = col.apply(format_timedelta_)
        elif _is_float(col):
            df[c] = col.apply(format_float_)
        elif _is_bool(col):
            df[c] = col.apply(format_bool_)
        elif _is_string(col):
            df[c] = col.apply(format_string_)
    # replace any remaining NaN values
    return df.fillna(na_rep)
