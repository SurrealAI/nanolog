import sys
import nanolog as nl
import pytest


def test_time2str():
    print(nl.time2str('current time: YMD HMS'))
    print(nl.time2str('MY@HM'))
    print(nl.time2str('YMD, MD, YM, HM, MS'))


@pytest.mark.parametrize('backend', ['thirdparty', 'builtin'])
def test_prettyprint(backend):
    nl.set_pprint_backend(backend)
    l1 = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
    l1.insert(0, l1[:])
    l2 = ['SPAM', 'EGGS', 'LUMBERJACK', 'KNIGHTS', 'NI']
    l2.insert(0, l2)

    nl.pprint(l1, '<->', l2, '<=>', l1, end='\n--\n', width=30, compact=True)

    nl.pprintfmt('{0}<->{var:.3f}<=>{1}<->{0}',
                 l1, l2, var=1/7.,
                 end='\n--\n', width=30, compact=True)


def test_pbanner():
    nl.pbanner('my', 3, 'world', symbol='!', banner_len=16, banner_lines=3)
    nl.pbanner(banner_len=16, banner_lines=2)
    nl.pbanner('my', 'critical', 'case', symbol='<*_*>',
               banner_len=16, banner_lines=6, file=sys.stderr)
    nl.pbannerfmt('{} {:0>5d} {var}',
                  'hello', 333, var=777,
                  symbol='!', banner_len=16, banner_lines=3)
    nl.pbannerfmt('{3}&{0}&{2}&{1}',
                  'a', 'b', 'c', 'd',
                  symbol='%#@.@', banner_len=16, banner_lines=6, file=sys.stderr)
