import pytest
import logging
import inspect
import nanolog as nl


def test_level_name():
    assert logging.getLevelName(20) == 'INFO'
    assert logging.getLevelName(23) == 'INFO3'
    assert logging.getLevelName(15) == 'DEBUG5'
    assert logging.getLevelName(37) == 'WARNING7'
    assert logging.getLevelName(61) == 'LEVEL61'
    assert nl.get_level_number('INFO') == 20
    assert nl.get_level_number('INFO3') == 23
    assert nl.get_level_number('WARNING7') == 37
    assert nl.get_level_number('DEBUG5') == 15
    assert nl.get_level_number('LEVEL17') == 17


@pytest.fixture
def logger():
    return nl.Logger.create_logger(
        'main',
        stream='out',
        level='debug5',
        show_level=False,
        format='{name} {asctime} {filename:>16s} {funcName}() {lineno} {levelname}\n',
        time_format='MDY@HMS',
    )


def test_constants():
    from nanolog.logger import _print_constants
    if 0:
        _print_constants()  # generate constants.py


def test_doc(logger):
    print(inspect.getdoc(logger.debug5))
    print(inspect.getdoc(logger.debugfmt5))
    print(inspect.getdoc(logger.infobanner))
    print(inspect.getdoc(logger.errorbanner2))
    print(inspect.getdoc(logger.criticalbanner))
    print(inspect.getdoc(logger.debugbannerfmt3))


def test_banner(logger):
    logger.infobanner3('my', 3, 'world', symbol='!',
                       banner_len=16, banner_lines=3)
    logger.infobanner3(banner_len=16, banner_lines=2)
    logger.criticalbanner('my', 'critical', 'case', symbol='<*_*>',
                           banner_len=16, banner_lines=6)


def test_bannerfmt(logger):
    logger.infobannerfmt3('{} {:0>5d} {var}',
                          'hello', 333, var=777,
                          symbol='!', banner_len=16, banner_lines=3)
    logger.errorbannerfmt('{3}&{0}&{2}&{1}',
                          'a', 'b', 'c', 'd',
                          symbol='<*_*>', banner_len=16, banner_lines=6)


def test_methods(logger):
    # print([_method for _method in dir(logger) if not _method.startswith('__')])
    logger.info7('my', 3, 'world', 1/16.)  # just like print
    logger.warningfmt('{}, we are {:.3f} miles from {planet}',
                      'Houston', 17/7, planet='Mars')  # just like str.format

    logger.error('this', 'an', 'error')
    try:
        1/0
    except Exception as e:
        logger.exception('myexc', 'yo', exc=e)
    logger.banner(logger.WARNING3, 'yoyoyoo', symbol='%')
    logger.criticalfmt('Client format {:0>5d} - {:?<9}', 21, 'asdiojfoigj')
    logger.debugfmt5('debugger {:0>5d} - {:?<9}', 42, 'asodjfaisdfisaj')


def test_formatting(logger):
    log=logger
    def f():
        log.infofmt7('yo {:.3f} info7', 1/17)
        log.criticalfmt('yo crit {:.2e} {}', 3**0.5, {'x':3})
        log.info7('yo {:.3f} info7', 1/17)
        log.critical('yo crit {:.2e} {}', 3**0.5, {'x':3})

    def g():
        log.info3('yo info3')
        log.warning('yo warn')

    f()
    g()
    f()
    log.infobanner('Yo', symbol='!', banner_len=50)
    # log.infobanner3('Yo', sep='!', repeat=50)
