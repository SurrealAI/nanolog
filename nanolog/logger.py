import os
import sys
import io
import re
import traceback
import inspect
from .printing import get_time_formatter, banner, bannerfmt
import logging as _logging


def _get_level_names():
    names = {}
    for i in range(1, 10):
        names[_logging.DEBUG + i] = 'DEBUG'+str(i)
        names[_logging.INFO + i] = 'INFO'+str(i)
        names[_logging.WARNING + i] = 'WARNING'+str(i)
        names[_logging.ERROR + i] = 'ERROR'+str(i)
        names[_logging.CRITICAL + i] = 'CRITICAL'+str(i)
    # add to standard lib
    for level, name in names.items():
        setattr(_logging, name, level)
    return names


_LEVEL_NAMES = _get_level_names()


_LEVEL_NAMES.update({
    _logging.CRITICAL: 'CRITICAL',
    _logging.ERROR: 'ERROR',
    _logging.WARNING: 'WARNING',
    _logging.INFO: 'INFO',
    _logging.DEBUG: 'DEBUG',
})


def get_level_name(level_number):
    """
    Args:
        level_number: int

    Returns:
        string name
    """
    if isinstance(level_number, str):
        return level_number
    assert isinstance(level_number, int)
    return _LEVEL_NAMES.get(level_number, 'LEVEL{}'.format(level_number))


def get_level_number(level_name):
    """
    Args:
        level_name: string. Will be converted to upper case.
            e.g. INFO, INFO5, DEBUG3, CRITICAL, LEVEL55, LEVEL32

    Returns:
        level number
    """
    if isinstance(level_name, int):
        return level_name
    level_name = level_name.upper()
    if hasattr(_logging, level_name):
        return getattr(_logging, level_name)
    else:
        try:
            if not level_name.startswith('LEVEL'):
                raise ValueError
            else:
                return int(level_name[len('LEVEL'):])
        except:
            raise ValueError('invalid level name: ' + level_name)


# hack stdlib function to enable better printing
_logging.getLevelName = get_level_name


# http://stackoverflow.com/questions/12980512/custom-logger-class-and-correct-line-number-function-name-in-log
# From python 3.5 source code:
# _srcfile is used when walking the stack to check when we've got the first
# caller stack frame, by skipping frames whose filename is that of this
# module's source. It therefore should contain the filename of this module's
# source file.
# Ordinarily we would use __file__ for this, but frozen modules don't always
# have __file__ set, for some reason (see Issue #21736). Thus, we get the
# filename from a handy code object from a function defined in this module.
# (There's no particular reason for picking get_level_name.)
#
_srcfile = os.path.normcase(get_level_name.__code__.co_filename)


def _expand_args(arg1, arg2):
    "Helper for add_file_handler and add_stream_handler"
    if not isinstance(arg1, list):
        arg1 = [arg1]
    if not isinstance(arg2, list):
        arg2 = [arg2]
    if len(arg1) == 1:
        # extend to the same length list as arg2
        arg1 = arg1 * len(arg2)
    if len(arg2) == 1:
        arg2 = arg2 * len(arg1)
    assert len(arg1) == len(arg2), \
        '{} and {} size mismatch'.format(arg1, arg2)
    return zip(arg1, arg2)


def _expand_arg(arg):
    "expand an arg into a singleton list"
    if isinstance(arg, list):
        return arg
    else:
        return [arg]


def _parse_level_name(level_name):
    "_MethodGenerator helper"
    level_name = level_name.lower()
    m = re.match('^([a-z]+)([0-9]*)$', level_name)
    assert m, 'INTERNAL ERROR'
    # 'info', '5' or ''
    return m.group(1), m.group(2)


class _MethodGenerator(type):
    def __new__(cls, cls_name, bases, method_dict):

        def _generate(level_number):
            # 'info', '5' or ''
            level_name = get_level_name(level_number)
            lname, lnum = _parse_level_name(level_name)

            def _log(self, *msg, **kwargs):
                """
                logging at severity {} (level {})

                Args:
                    *msg: as you would use print()
                    **kwargs:
                      - sep: separator symbol between *msg, the same as print()
                      - exc_info, stack_info, extra: logging builtin keywords
                """
                return self.log(level_number, *msg, **kwargs)
            _log.__doc__ = _log.__doc__.format(level_name, level_number)

            def _logfmt(self, msg, *args, **kwargs):
                """
                logging with formatting string at severity {} (level {})

                Args:
                    msg: "{{}}"-style format string
                    *args: positional args for the format string
                    **kwargs:
                      keyword args for the format string, except for
                      "exc_info", "stack_info", "extra" logging keywords
                """
                return self.logfmt(level_number, msg, *args, **kwargs)
            _logfmt.__doc__ = _logfmt.__doc__.format(level_name, level_number)

            def _banner(self, *msg,
                        sep=' ', symbol='=', banner_len=20, banner_lines=1):
                """
                Display a banner line or block with your message in the middle
                logging at severity {} (level {})

                Args:
                  sep: separator between *msg, same as in print()
                  symbol: banner symbol
                  banner_len: length of the banner symbols (excluding message itself)
                  banner_lines: number of the banner lines, ideally an odd number
                """
                return self.banner(
                    level_number, *msg,
                    sep=sep,
                    symbol=symbol,
                    banner_len=banner_len,
                    banner_lines=banner_lines
                )
            _banner.__doc__ = _banner.__doc__.format(level_name, level_number)

            def _bannerfmt(self, msg, *args,
                          symbol='=', banner_len=20, banner_lines=1, **kwargs):
                """
                Display a banner line or block with your message in the middle.
                logging at severity {} (level {})
                Message is formatted in {{}}-style with *args and **kwargs
                Other banner settings are the same as banner() method

                Args:
                  msg: "{{}}"-style format string
                  *args: positional args for the format string
                  **kwargs: keyword args for the format string, except for
                      "exc_info", "stack_info", "extra" logging keywords
                  symbol: banner symbol
                  banner_len: length of the banner symbols (excluding message itself)
                  banner_lines: number of the banner lines, ideally an odd number
                """
                return self.bannerfmt(
                    level_number, msg, *args,
                    symbol=symbol,
                    banner_len=banner_len,
                    banner_lines=banner_lines,
                    **kwargs
                )
            _bannerfmt.__doc__ = _bannerfmt.__doc__.format(level_name, level_number)

            method_dict[lname+lnum] = _log
            method_dict[lname+'fmt'+lnum] = _logfmt
            method_dict[lname+'banner'+lnum] = _banner
            method_dict[lname+'bannerfmt'+lnum] = _bannerfmt

        # generate all methods from DEBUG, DEBUG2, DEBUG3, ..., CRITICAL9
        for level_number in range(10, 60):
            _generate(level_number)

        for level, name in _LEVEL_NAMES.items():
            method_dict[name] = level
        return super().__new__(cls, cls_name, bases, method_dict)
        

class Logger(metaclass=_MethodGenerator):
    """
    logger = Logger(logger)
    fully supports positional/keyword new formatter string syntax

    Example:
    
    ::
        logger.info("Float {1:>7.3f} and int {0} with {banana} and {apple:.6f}", 
                    66, 3.141592, apple=7**.5, banana='str')
        # if the first arg isn't a format string, treat as if print statement
        # you can specify a `sep=` arg under this case. `sep` defaults to space
        logger.info({3:'apple', 4:'banana'}, 4.5, 'asdf')
        logger.info('I am not a format string', 66, {'key':'value'}, sep=', ')
    
    Custom verbosity level. The higher the more strings printed. 
    log.info1(), .info2() ... info5(). 
    corresponding levels: INFO1 to INFO5

    https://docs.python.org/3/library/logging.html#logrecord-attributes
    # print out all format attributes
    fmt_string = ''
    for s in LoggerPro.FORMAT_ATTRS:
        fmt_string += '{0}={{{0}}}\n'.format(s)
    print(fmt_string)
    log.set_formatter((fmt_string, None))
    log.info('HELLO', 'WORLD!')
    """
    FORMAT_ATTRS = ['pathname', 'filename', 'lineno', 'funcName', 'module',
                    'process', 'processName', 'thread', 'threadName',
                    'created', 'relativeCreated', 'msecs',
                    'levelname', 'levelno', 'asctime', 'message']
    
    def __init__(self, logger):
        self.logger = logger
        
    def __getattr__(self, attr):
        "Access wrapped logger methods transparently"
        if attr in dir(self):
            return object.__getattribute__(self, attr)
        else:
            return getattr(self.logger, attr)

    def is_enabled_for(self, level):
        """
        same as logging.isEnabledFor

        Args:
            level: level name (string) or number (int)
        """
        level = get_level_number(level)
        return self.logger.isEnabledFor(level)

    def _process_msg(self, *msg, **kwargs):
        # if 'sep' is provided, we will use the custom separator instead
        sep = kwargs.pop('sep', ' ')
        # e.g. "{}, {}, {}" if sep = ", "
        msg = sep.join([u'{}'] * len(msg)).format(*msg)
        return msg, kwargs

    def _process_msg_fmt(self, msg, *args, **kwargs):
        fmt_kwargs = {}
        for key, value in kwargs.copy().items():
            if not key in ['exc_info', 'stack_info', 'extra']:
                fmt_kwargs[key] = value
                # must remove unsupported keyword for internal args
                kwargs.pop(key)
        msg = msg.format(*args, **fmt_kwargs)
        return msg, kwargs

    @staticmethod
    def exception2str(exc):
        buf = io.StringIO()
        traceback.print_exception(
            type(exc),
            exc,
            exc.__traceback__,
            file=buf
        )
        buf = buf.getvalue().strip()
        return '\n'.join(['ERROR> ' + line for line in buf.split('\n')])

    def exception(self, msg, *args, exc, **kwargs):
        """
        Logs a message with level ERROR on this logger. 
        Exception info is always added to the logging message. 

        Args:
            exc: the exception value that extends BaseException

        Warning:
            Only Python3 supports exception.__traceback__
        """
        if self.is_enabled_for('ERROR'):
            msg, kwargs = self._process_msg(msg, *args, **kwargs)
            msg += '\n'
            if isinstance(exc, str):  # see LoggerplexClient
                msg += exc
            else:
                msg += self.exception2str(exc)
            self.logger.error(msg, **kwargs)
    
    def log(self, level, *msg, **kwargs):
        """
        Log with user-defined level, e.g. INFO3, DEBUG5, WARNING7

        Args:
            level: logging level name or number
            *msg: as you would use print()
            **kwargs:
              - sep: separator symbol between *msg, the same as print()
              - exc_info, stack_info, extra: logging builtin keywords
        """
        if self.is_enabled_for(level):
            msg, kwargs = self._process_msg(*msg, **kwargs)
            # self.logger.log(level, msg, **kwargs)
            self._log(level, msg, **kwargs)

    def logfmt(self, level, msg, *args, **kwargs):
        """
        Log with user-defined level, e.g. INFO3, DEBUG5, WARNING7

        Args:
            level: logging level name or number
            msg: "{}"-style format string
            *args: positional args for the format string
            **kwargs: keyword args for the format string, except for
              "exc_info", "stack_info", "extra" logging keywords
        """
        if self.is_enabled_for(level):
            msg, kwargs = self._process_msg_fmt(msg, *args, **kwargs)
            # self.logger.log(level, msg, **kwargs)
            self._log(level, msg, **kwargs)

    def banner(self, level, *msg,
               sep=' ', symbol='=', banner_len=20, banner_lines=1):
        """
        Display a banner line or block with your message in the middle

        Args:
          level: logging level name or number
          sep: separator between *msg, same as in print()
          symbol: banner symbol
          banner_len: length of the banner symbols (excluding message itself)
          banner_lines: number of the banner lines, ideally an odd number

        Example:
          # long unbroken line of '!'
          logger.banner(INFO, symbol='!', bannerlen=80)
          # !!!!!!!!! my hello world !!!!!!!!!
          logger.banner(DEBUG2, 'my', 'hello', 'world', symbol='!', banner_len=10)
        """
        if self.is_enabled_for(level):
            msg = banner(
                *msg, sep=sep, symbol=symbol,
                banner_len=banner_len, banner_lines=banner_lines
            )
            self._log(level, msg)

    def bannerfmt(self, level, msg, *args,
                  symbol='=', banner_len=20, banner_lines=1, **kwargs):
        """
        Display a banner line or block with your message in the middle.
        Message is formatted in {}-style with *args and **kwargs
        Other banner settings are the same as banner() method

        Args:
          level: logging level name or number
          msg: "{}"-style format string
          *args: positional args for the format string
          **kwargs: keyword args for the format string, except for
              "exc_info", "stack_info", "extra" logging keywords
          symbol: banner symbol
          banner_len: length of the banner symbols (excluding message itself)
          banner_lines: number of the banner lines, ideally an odd number
        """
        if self.is_enabled_for(level):
            msg, kwargs = self._process_msg_fmt(msg, *args, **kwargs)
            msg = banner(
                msg, symbol=symbol,
                banner_len=banner_len, banner_lines=banner_lines
            )
            self._log(level, msg, **kwargs)

    def remove_all_handlers(self):
        for handle in self.logger.handlers:
            self.logger.removeHandler(handle)

    def configure(self,
                  level=None, 
                  file_name=None,
                  file_mode='a',
                  format=None,
                  time_format=None,
                  show_level=False,
                  stream=None,
                  reset_handlers=False):
        """
        Args:
          level: None to retain the original level of the logger
          file_name: None to print to console only
          file_mode: 'w' to override a file or 'a' to append
          format: `{}` style logging format string, right after level name
          time_format:
            - `dhms`: %m/%d %H:%M:%S
            - `dhm`: %m/%d %H:%M
            - `hms`: %H:%M:%S
            - `hm`: %H:%M
            - if contains '%', will be interpreted as a time format string
            - None
          show_level: if True, display `INFO> ` before the message
          stream: 
            - stream object: defaults to sys.stderr
            - str: "out", "stdout", "err", or "stderr"
            - None: do not print to any stream
          reset_handlers: True to remove all old handlers

        Notes:
            log format rules:
            levelname> [preamble] ...your message...

            If show_level is True, `levelname> ` will be the first
            If format is None and time_format is None, no preamble prints
            If format is None and time_format specified, print time preamble
            If format specified, time_format will take effect only if
                '{asctime}' is contained in the format.
            E.g. if format is empty string, no preamble prints even if
            time_format is set.

        References:
        - for format string:
            https://docs.python.org/3/library/logging.html#logrecord-attributes
        - for time_format string:
            https://docs.python.org/3/library/time.html#time.strftime

        Warning:
          always removes all previous handlers
        """
        if reset_handlers:
            self.remove_all_handlers()
        if level:
            if isinstance(level, str):  # "INFO", "WARNING"
                level = level.upper()
                level = getattr(self, level)
            self.logger.setLevel(level)
        self.add_stream_handler(stream, format, time_format, show_level)
        self.add_file_handler(file_name, file_mode,
                              format, time_format, show_level)
        return self
    
    @classmethod
    def get_logger(cls, name,
                   level=None,
                   file_name=None,
                   file_mode='a',
                   format=None,
                   time_format=None,
                   show_level=False,
                   stream=None,
                   reset_handlers=False):
        """
        Returns:
          a logger with the same config args as `.configure(...)`
          - if the logger already exists, retain its previous level
          - if new logger, set to INFO as default level

        Note:
          set `propagate` to False to prevent double-printing
          https://stackoverflow.com/questions/11820338/replace-default-handler-of-python-logger
        """
        if not Logger.exists(name) and level is None:
            level = _logging.INFO
        raw_logger = _logging.getLogger(name)
        raw_logger.propagate = False
        return cls(raw_logger).configure(
            level=level,
            file_name=file_name,
            file_mode=file_mode,
            format=format,
            time_format=time_format,
            show_level=show_level,
            stream=stream,
            reset_handlers=reset_handlers
        )
    
    @classmethod
    def wrap_logger(cls, logger):
        """
        Args:
          logger: if string, logging.getLogger(). Else wrap and return.
        """
        if isinstance(logger, str):
            logger = _logging.getLogger(logger)
        return cls(logger)

    def _get_formatter(self, format, time_format, show_level):
        levelname = '{levelname}> ' if show_level else ''
        if format is None:
            if time_format is not None:
                fmt = '{asctime} '
            else:
                fmt = ''
        else:
            fmt = format
        return _logging.Formatter(
            fmt=fmt + levelname + '{message}',
            datefmt=get_time_formatter(time_format),
            style='{'
        )
    
    def add_file_handler(self,
                         file_name,
                         file_mode='a',
                         format=None,
                         time_format=None,
                         show_level=False):
        """
        Args:
            file_name: one string or a list of strings
            file_mode: one mode or a list of modes, must match len(file_name)
        """
        if not file_name:
            return
        file_name = os.path.expanduser(file_name)
        formatter = self._get_formatter(format, time_format, show_level)
        for name, mode in _expand_args(file_name, file_mode):
            handler = _logging.FileHandler(name, mode)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self

    def add_stream_handler(self,
                           stream,
                           format=None,
                           time_format=None,
                           show_level=False):
        """
        Args:
            stream: 
            - stream object: e.g. sys.stderr
            - str: "out", "stdout", "err", or "stderr"
            - a list of the above to add multiple strings
        """
        if not stream:
            return
        formatter = self._get_formatter(format, time_format, show_level)
        for stream in _expand_arg(stream):
            if isinstance(stream, str):
                if stream in ['out', 'stdout']:
                    stream = sys.stdout
                elif stream in ['err', 'stderr']:
                    stream = sys.stderr
                else:
                    raise ValueError('Unsupported stream name: '+stream)
            handler = _logging.StreamHandler(stream)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        return self
    
    def set_formatter(self, formatter, time_formatter=None):
        """
        Sets a custom formatter for *all* handlers.
        https://docs.python.org/3/library/logging.html#formatter-objects

        Args:
          formatter: format string (style is `{}`) or instance of logging.Formatter
          time_formatter: time format string
            will be no-op if `formatter` is instance of logging.Formatter
            please see `nanolog.printing.get_time_formatter for aliases

        References:
        - for fmt string:
            https://docs.python.org/3/library/logging.html#logrecord-attributes
        - for datefmt string:
            https://docs.python.org/3/library/time.html#time.strftime
        """
        if isinstance(formatter, str):
            if time_formatter:
                datefmt = get_time_formatter(time_formatter)
            else:
                datefmt = None
            formatter = _logging.Formatter(formatter, datefmt=datefmt, style='{')
        elif not isinstance(formatter, _logging.Formatter):
            raise TypeError('formatter must be either an instance of '
                    'logging.Formatter or a tuple of (fmt, datefmt) strings')
        for handler in self.logger.handlers:
            handler.setFormatter(formatter)

    @staticmethod
    def all_loggers():
        """
        http://stackoverflow.com/questions/13870555/how-to-clear-reset-all-configured-logging-handlers-in-python
        
        Returns: 
            a dict of all registered loggers under root
        """
        return _logging.Logger.manager.loggerDict
    
    @staticmethod
    def exists(name):
        """
        Check whether a logger exists
        """
        return name in Logger.all_loggers()

    # ================================================
    # copy stdlib logging source code here to ensure that line numbers
    # and file locations are correct in the log message
    # http://stackoverflow.com/questions/12980512/custom-logger-class-and-correct-line-number-function-name-in-log
    # ================================================
    def _findCaller(self, stack_info=False):
        # Find the stack frame of the caller so that we can note the source
        # file name, line number and function name.
        f = _logging.currentframe()
        #On some versions of IronPython, currentframe() returns None if
        #IronPython isn't run with -X:Frames.
        if f is not None:
            f = f.f_back
        rv = "(unknown file)", 0, "(unknown function)", None
        while hasattr(f, "f_code"):
            co = f.f_code
            filename = os.path.normcase(co.co_filename)
            if filename == _srcfile:
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def _log(self, level, msg, args=tuple(), exc_info=None, extra=None, stack_info=False):
        # Low-level logging routine which creates a LogRecord and then calls
        # all the handlers of this logger to handle the record.
        sinfo = None
        if _srcfile:
            #IronPython doesn't track Python frames, so findCaller raises an
            #exception on some versions of IronPython. We trap it here so that
            #IronPython can use logging.
            try:
                fn, lno, func, sinfo = self._findCaller(stack_info)
            except ValueError: # pragma: no cover
                fn, lno, func = "(unknown file)", 0, "(unknown function)"
        else: # pragma: no cover
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.logger.makeRecord(self.logger.name, level, fn, lno, msg, args,
                                        exc_info, func, extra, sinfo)
        self.logger.handle(record)
