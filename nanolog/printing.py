"""
Printing utils:

- Context manager-based printing streams.
- Convert data structures to pretty string representation. 
"""

import os
import sys
import datetime
import time
import pprint as _pprint_builtin
import prettyprinter as _pprint_thirdparty
from collections import abc
from io import StringIO


_PP_BACKEND = _pprint_thirdparty
# global default configs
_PP_CONFIG = {
    'indent': 1,
    'width': 80,
    'depth': None,
    'compact': False
}

PP_DEFAULT = '__default__'  # use default config value


def set_pprint_backend(backend):
    """
    Args:
        backend (string):
        - "builtin" for python builtin prettyprint
        - "thirdparty" (default) for Kaikkonen's prettyprinter
            https://github.com/tommikaikkonen/prettyprinter
    """
    global _PP_BACKEND
    backend = backend.lower()
    assert backend in ['builtin', 'thirdparty']
    if backend == 'builtin':
        _PP_BACKEND = _pprint_builtin
    else:
        _PP_BACKEND = _pprint_thirdparty


def set_pprint_config(indent=PP_DEFAULT,
                      width=PP_DEFAULT,
                      depth=PP_DEFAULT,
                      compact=PP_DEFAULT):
    kwargs = dict(indent=indent, width=width, depth=depth, compact=compact)
    for key, value in kwargs.items():
        if value != PP_DEFAULT:
            _PP_CONFIG[key] = value


def _pformat(obj, indent, width, depth, compact, *, _leave_number):
    if isinstance(obj, str):
        return obj
    # don't convert number to string if we pass it to str.format()
    if isinstance(obj, (int, float)) and _leave_number:
        return obj
    kwargs = dict(indent=indent, width=width, depth=depth, compact=compact)
    for key, value in kwargs.items():
        if value == PP_DEFAULT:
            kwargs[key] = _PP_CONFIG[key]
    return _PP_BACKEND.pformat(obj, **kwargs)


def printerr(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def pprint(*objs,
           sep=' ', end='\n', file=sys.stdout, flush=False,
           indent=PP_DEFAULT, width=PP_DEFAULT, depth=PP_DEFAULT, compact=PP_DEFAULT
           ):
    """
    print() with prettyprint
    """
    print(
        pprintstr(*objs, sep=sep,
                  indent=indent, width=width, depth=depth, compact=compact),
        end=end, file=file, flush=flush
    )


def pprintstr(*objs, sep=' ',
              indent=PP_DEFAULT, width=PP_DEFAULT, depth=PP_DEFAULT, compact=PP_DEFAULT
              ):
    pf = lambda obj: _pformat(
        obj, indent, width, depth, compact, _leave_number=False)
    return sep.join(map(pf, objs))


def pprintfmt(msg, *fmt_args,
              end='\n', file=sys.stdout, flush=False,
              indent=PP_DEFAULT, width=PP_DEFAULT, depth=PP_DEFAULT, compact=PP_DEFAULT,
              **fmt_kwargs):
    """
    Equivalent to print(msg.format(*args, **kwargs)) with prettyprint
    """
    print(
        pprintfmtstr(msg, *fmt_args,
                     indent=indent, width=width, depth=depth, compact=compact,
                     **fmt_kwargs),
        end=end, file=file, flush=flush
    )


def pprintfmtstr(msg, *fmt_args,
                 indent=PP_DEFAULT, width=PP_DEFAULT, depth=PP_DEFAULT, compact=PP_DEFAULT,
                 **fmt_kwargs):
    """
    Equivalent to print(msg.format(*args, **kwargs)) with prettyprint

    Warnings:
        all positional and keyword args to str.format will be converted to string
        first, which means float/int will not be
    """
    pf = lambda obj: _pformat(
        obj, indent, width, depth, compact, _leave_number=True)
    fmt_args = map(pf, fmt_args)
    fmt_kwargs = {key: pf(value) for key, value in fmt_kwargs.items()}
    return msg.format(*fmt_args, **fmt_kwargs)

# ---------------- shorthands -----------------
perr = printerr
pp = pprint
pps = pprintstr
ppf = pprintfmt
ppfs = pprintfmtstr


# ---------------- banners -----------------
def _banner(msg, symbol, banner_len, banner_lines):
    "helper for banner() and bannerfmt()"
    # repeat `symbol`, cut in middle if necessary
    half_len = banner_len // 2
    half_banner = (symbol * (half_len // len(symbol))
                   + symbol[:half_len % len(symbol)])
    assert len(half_banner) == half_len, 'INTERNAL ERROR'
    central_line = u'{half_banner}{space}{msg}{space}{half_banner}'.format(
        half_banner=half_banner,
        msg=msg,
        space=' ' if msg else ''
    )
    full_len = len(central_line)  # including message
    banner_lines -= 1
    surround_banner = (symbol * (full_len // len(symbol))
                       + symbol[:full_len % len(symbol)])
    before_banner = [surround_banner] * (banner_lines // 2)
    after_banner = [surround_banner] * (banner_lines - banner_lines // 2)
    full_banner = before_banner + [central_line] + after_banner
    return '\n'.join(full_banner)


def banner(*msg, sep=' ', symbol='=', banner_len=20, banner_lines=1):
    """
    A banner line or block with your message in the middle

    Args:
      sep: separator between *msg, same as in print()
      symbol: banner symbol
      banner_len: length of the banner symbols (excluding message itself)
      banner_lines: number of the banner lines, ideally an odd number

    Example:
      # long unbroken line of '!'
      banner(symbol='!', bannerlen=80)
      # !!!!!!!!! my hello world !!!!!!!!!
      banner('my', 'hello', 'world', symbol='!', banner_len=10)
    """
    msg = sep.join([u'{}'] * len(msg)).format(*msg)
    return _banner(msg, symbol, banner_len, banner_lines)


def pbanner(*msg, sep=' ', symbol='=', banner_len=20, banner_lines=1,
            end='\n', file=sys.stdout, flush=False):
    print(banner(*msg, sep=sep,
        symbol=symbol, banner_len=banner_len, banner_lines=banner_lines
    ), end=end, file=file, flush=flush)


def bannerfmt(msg, *fmt_args, symbol='=', banner_len=20, banner_lines=1,
              **fmt_kwargs):
    """
    A banner line or block with your message in the middle.
    Message is formatted in {}-style with *args and **kwargs
    Other banner settings are the same as banner() method

    Args:
      msg: "{}"-style format string
      *fmt_args: positional args for the format string
      **fmt_kwargs: keyword args for the format string
      symbol: banner symbol
      banner_len: length of the banner symbols (excluding message itself)
      banner_lines: number of the banner lines, ideally an odd number
    """
    msg = msg.format(*fmt_args, **fmt_kwargs)
    return _banner(msg, symbol, banner_len, banner_lines)


def pbannerfmt(msg, *fmt_args, symbol='=', banner_len=20, banner_lines=1,
               end='\n', file=sys.stdout, flush=False, **fmt_kwargs):
    print(bannerfmt(msg, *fmt_args,
        symbol=symbol, banner_len=banner_len, banner_lines=banner_lines, **fmt_kwargs
    ), end=end, file=file, flush=flush)

# ---------------- time formatting -----------------
def get_time_formatter(formatter):
    """
    Convenient aliases for common time formatter.
    For complete time format spec, please refer to
    https://docs.python.org/3/library/time.html#time.strftime

    Args:
      formatter: y=year, d=day, h=hour, m=minute, s=second
        any combination of
        'MDY' 'YMD' 'DMY' 'YDM' 'MY' 'YM' 'MD' 'DM'
        'HMS' 'HM' 'MS'
        formatted as in "month-day-year" and "hour:minute:second"

    Examples:
      "MDY HMS" => "12-25-18 16:38:05"
      "HM@MD" => "16:38@12-25"
      "time: YMD MS" => "time: 18-12-25 38:05"

    Returns:
      time format string with %
    """
    return (
        formatter
            .replace('MDY', '%m-%d-%y')
            .replace('YMD', '%y-%m-%d')
            .replace('DMY', '%d-%m-%y')
            .replace('YDM', '%y-%d-%m')
            .replace('MY', '%m-%y')
            .replace('YM', '%y-%m')
            .replace('MD', '%m-%d')
            .replace('DM', '%d-%m')
            .replace('HMS', '%H:%M:%S')
            .replace('HM', '%H:%M')
            .replace('MS', '%M:%S')
    )


def time2str(formatter):
    """
    https://docs.python.org/3/library/time.html#time.strftime
    %m - month; %d - day; %y - year
    %H - 24 hr; %I - 12 hr; %M - minute; %S - second; %p - AM or PM

    See `get_time_formatter` for convenient aliases in formatter

    Returns:
        string of the current time formatted with `formatter`
    """
    if '%' not in formatter:
        formatter = get_time_formatter(formatter)
    return time.strftime(formatter)


def seconds2str(seconds):
    "Convert seconds to str `HH:MM:SS`"
    return datetime.timedelta(seconds=seconds)


def dict2str(D,
             sep='=',
             item_sep=', ',
             key_format='',
             value_format='',
             enclose=('{', '}')):
    """
    Pretty string representation of a dictionary. Works with Unicode.

    Args:
      sep: "key `sep` value"
      item_sep: separator between key-value pairs
      key_format: same format string as in str.format()
      value_format: same format string as in str.format()
      enclose: a 2-tuple of enclosing symbols
    """
    assert len(enclose) == 2
    itemstrs = []
    for key, value in D.items():
        itemstrs.append(u'{{:{}}} {} {{:{}}}'
                        .format(key_format, sep, value_format)
                        .format(key, value))
    return enclose[0] + item_sep.join(itemstrs) + enclose[1]


def list2str(L,
             sep=', ',
             item_format='',
             enclose=None):
    """
    Pretty string representation of a list or tuple. Works with Unicode.

    Args:
      sep: separator between two list items
      item_format: same format string as in str.format()
      enclose: a 2-tuple of enclosing symbols. 
          default: `[]` for list and `()` for tuple.
    """
    if enclose is None:
        if isinstance(L, tuple):
            enclose = ('(', ')')
        else:
            enclose = ('[', ']')
    else:
        assert len(enclose) == 2
    item_format = u'{{:{}}}'.format(item_format)
    itemstr = sep.join(map(lambda s: item_format.format(s), L))
    return enclose[0] + itemstr + enclose[1]


# ---------------- print redirections -----------------
class PrintRedirection:
    """
    Context manager: temporarily redirects stdout and stderr
    """
    def __init__(self, stdout=None, stderr=None):
        """
        Args:
          stdout: if None, defaults to sys.stdout, unchanged
          stderr: if None, defaults to sys.stderr, unchanged
        """
        if stdout is None:
            stdout = sys.stdout
        if stderr is None:
            stderr = sys.stderr
        self._stdout, self._stderr = stdout, stderr

    def __enter__(self):
        self._old_out, self._old_err = sys.stdout, sys.stderr
        self._old_out.flush()
        self._old_err.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self
            
    def __exit__(self, exc_type, exc_value, traceback):
        self.flush()
        # restore the normal stdout and stderr
        sys.stdout, sys.stderr = self._old_out, self._old_err
    
    def flush(self):
        "Manually flush the replaced stdout/stderr buffers."
        self._stdout.flush()
        self._stderr.flush()


class PrintFile(PrintRedirection):
    """
    Print to file and save/close the handle at the end.
    """
    def __init__(self, out_file=None, err_file=None):
        """
        Args:
          out_file: file path
          err_file: file path. If the same as out_file, print both stdout 
              and stderr to one file in order.
        """
        self.out_file, self.err_file = out_file, err_file
        if out_file:
            out_file = os.path.expanduser(out_file)
            self.out_file = open(out_file, 'w')
        if err_file:
            err_file = os.path.expanduser(err_file)
            if err_file == out_file: # redirect both stdout/err to one file
                self.err_file = self.out_file
            else:
                self.err_file = open(os.path.expanduser(err_file), 'w')

        super().__init__(stdout=self.out_file, stderr=self.err_file)
    
    def __exit__(self, *args):
        super().__exit__(*args)
        if self.out_file:
            self.out_file.close()
        if self.err_file:
            self.err_file.close()


def PrintSuppress(no_out=True, no_err=True):
    """
    Args:
      no_out: stdout writes to sys.devnull
      no_err: stderr writes to sys.devnull
    """
    out_file = os.devnull if no_out else None
    err_file = os.devnull if no_err else None
    return PrintFile(out_file=out_file, err_file=err_file)


class PrintString(PrintRedirection):
    """
    Redirect stdout and stderr to strings.
    """
    def __init__(self):
        self.out_stream = StringIO()
        self.err_stream = StringIO()
        super().__init__(stdout=self.out_stream, stderr=self.err_stream)
    
    def stdout(self):
        "Returns: stdout as one string."
        return self.out_stream.getvalue()
    
    def stderr(self):
        "Returns: stderr as one string."
        return self.err_stream.getvalue()
        
    def stdout_by_line(self):
        "Returns: a list of stdout line by line, ignore trailing blanks"
        return self.stdout().rstrip().split('\n')

    def stderr_by_line(self):
        "Returns: a list of stderr line by line, ignore trailing blanks"
        return self.stderr().rstrip().split('\n')

