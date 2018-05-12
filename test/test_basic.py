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


def test_methods():
    logger = nl.Logger.get_logger(
        'main',
        stream='out',
        level='warning',
        show_level=True,
        format='{name} {asctime} {filename:>16s} {funcName}() {lineno} {levelname} ',
        time_format='dhm',
    )

    print([_method for _method in dir(logger) if not _method.startswith('__')])

    logger.info('client')
    logger.info7('client')
    logger.error('this', 'an', 'error')
    try:
        1/0
    except Exception as e:
        logger.exception('myexc', 'yo', exc=e)
    logger.section('yoyoyoo', sep='%')
    logger.criticalfmt('Client format {:0>5d} - {:?<9}', 21, 'asdiojfoigj')
    logger.debugfmt5('debugger {:0>5d} - {:?<9}', 42, 'asodjfaisdfisaj')

    print(inspect.getdoc(logger.info7))
    print(inspect.getdoc(logger.debug3))


def test_formatting():
    log = nl.Logger.get_logger(
        'main',
        stream='out',
        level='info2',
        show_level=True,
        format='{name} {asctime} {filename:>16s} {funcName}() {lineno} {levelname} ',
        time_format='dhm',
    )

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
    log.infosection('Yo', sep='!', repeat=50)
    # log.infosection3('Yo', sep='!', repeat=50)
