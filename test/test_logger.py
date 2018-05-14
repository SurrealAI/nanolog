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
        format='{name} {asctime} {filename:>16s} {funcName}() {lineno} ${levelname}$\n',
        time_format='MDY@HMS',
    )


def test_doc(logger):
    print(inspect.getdoc(logger.debug))
    print(inspect.getdoc(logger.warningfmt5))
    print(inspect.getdoc(logger.infobanner))
    print(inspect.getdoc(logger.errorbanner2))
    print(inspect.getdoc(logger.criticalpp))
    print(inspect.getdoc(logger.debugppfmt3))


def test_log(logger):
    # print([_method for _method in dir(logger) if not _method.startswith('__')])
    logger.info7('my', 3, 'world', 1/16.)  # just like print
    logger.warning9('yo {:.3f} info7', 1/17)  # should NOT format!
    logger.debug3('SHOULD NOT SHOW!! logger level >= debug5')

    logger.error('this', 'an', 'error')
    try:
        1/0
    except Exception as e:
        logger.exception('myexc', 'yo', exc=e)
    logger.banner(logger.WARNING3, 'yoyoyoo', symbol='%')
    logger.critical('yo crit {:.2e} {}', 3**0.5, {'x':3})


def test_logfmt(logger):
    logger.infofmt7('yo {:.3f} info7', 1/17)
    logger.criticalfmt('yo crit {:.2e} {}', 3**0.5, {'x':3})
    logger.warningfmt('{}, we are {:.3f} miles from {planet}',
                      'Houston', 17/7, planet='Mars')  # just like str.format
    logger.errorfmt('Client format {:0>5d} - {:?<9}', 21, 'asdiojfoigj')
    logger.debugfmt5('debugger {:0>5d} - {:?<9}', 42, 'asodjfaisdfisaj')


def test_banner(logger):
    logger.infobanner3('my', 3, 'world', symbol='!',
                       banner_len=16, banner_lines=3)
    logger.infobanner3(banner_len=16, banner_lines=2)
    logger.criticalbanner('my', 'critical', 'case', symbol='<*_*>',
                          banner_len=16, banner_lines=6)
    logger.debugbanner('SHOULD NOT SHOW!! logger level >= debug5')


def test_bannerfmt(logger):
    logger.infobannerfmt3('{} {:0>5d} {var}',
                          'hello', 333, var=777,
                          symbol='!', banner_len=16, banner_lines=3)
    logger.errorbannerfmt('{3}&{0}&{2}&{1}',
                          'a', 'b', 'c', 'd',
                          symbol='<*_*>', banner_len=16, banner_lines=6)


def test_pp(logger):
    d1 = {'a': {'a': {'a': {'a': {'a': {'b': 10}}}}}}
    d2 = {'A': {'A': {'A': {'A': {'A': {'B': 10}}}}}}
    logger.debugpp5(d2, '<->', d1, compact=True)
    logger.warningpp('hello', d1, '<->', d2, width=10, depth=3)
    logger.errorpp7('<-err->', d2, width=35, compact=True)


def test_ppfmt(logger):
    d1 = {'a': {'a': {'a': {'a': {'a': {'b': 10}}}}}}
    d2 = {'A': {'A': {'A': {'A': {'A': {'B': 10}}}}}}
    logger.debugppfmt2('SHOULD', 'NOT', 'SHOW', d1)
    logger.warningppfmt5('compact D2->{2}, num={1:.3f}, D1->{0}',
                         d1, 1/7, d2,
                         width=10, depth=3, compact=True)
    logger.warningppfmt5('D2->{2}, num={1:.3f}, D1->{0}',
                         d1, 1/7, d2,
                         width=10, depth=3)
    logger.criticalppfmt('{myd2} myerr {myd2}', myd2=d2,
                         width=35, compact=True)


def test_set_level(logger):
    with logger.temp_level_scope(logger.ERROR5):
        logger.error4('my', 20, 'hello', 30, 'world')
    logger.error4('my', 20, 'hello', 30, 'world')


def test_throwaway():
    import logging
    log = logging.getLogger('abc.def')
    log.info('asdf {} {}', 3, 5)

