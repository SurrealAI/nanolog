import sys
import nanolog as nl
import pytest


def test_time2str():
    print(nl.time2str('current time: YMD HMS'))
    print(nl.time2str('MY@HM'))
    print(nl.time2str('YMD, MD, YM, HM, MS'))


@pytest.mark.parametrize('backend', ['builtin', 'thirdparty'])
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


def test_compact():
    data = {'10.22.197.3': [{'DBClientID': '2996e1a93ee6a9234808fa04e5a889ae2e1984f0', 'ClientType': 'local_scheduler', 'Deleted': False, 'LocalSchedulerSocketName': '/tmp/scheduler56853620', 'GPU': 0.0, 'CPU': 8.0, 'mujoco': 15.0, 'AuxAddress': '10.22.197.3:53895'}, {'DBClientID': '860f9b328bde40a5bae565943f76fc0ce8bcd640', 'ClientType': 'plasma_manager', 'Deleted': False, 'store_socket_name': '/tmp/plasma_store63002382', 'manager_socket_name': '/tmp/plasma_manager2032735', 'AuxAddress': '10.22.197.3:53895'}], '10.22.193.6': [{'DBClientID': '15d9e88a0228d07934f31ce5cfe3835afb94497d', 'ClientType': 'global_scheduler', 'Deleted': False}, {'DBClientID': '63fba70f2d7fd35611329b93f7c6f1c888c69cc4', 'ClientType': 'local_scheduler', 'Deleted': False, 'LocalSchedulerSocketName': '/tmp/scheduler73889199', 'GPU': 0.0, 'CPU': 2.0, 'AuxAddress': '10.22.193.6:25163'}, {'DBClientID': '90e66ecf88a7cfb5972bbdc31776aacbb022578b', 'ClientType': 'plasma_manager', 'Deleted': False, 'store_socket_name': '/tmp/plasma_store84158689', 'manager_socket_name': '/tmp/plasma_manager95601982', 'AuxAddress': '10.22.193.6:25163'}], '10.22.195.3': [{'DBClientID': 'df540889a36dc1324d6a85bf123f1f7f4f6ea1ba', 'ClientType': 'local_scheduler', 'Deleted': False, 'LocalSchedulerSocketName': '/tmp/scheduler86198036', 'GPU': 0.0, 'CPU': 8.0, 'mujoco': 15.0, 'AuxAddress': '10.22.195.3:57600'}, {'DBClientID': '9f569963466abda68b7d90192789e3fda2f32f8f', 'ClientType': 'plasma_manager', 'Deleted': False, 'store_socket_name': '/tmp/plasma_store77322023', 'manager_socket_name': '/tmp/plasma_manager90407822', 'AuxAddress': '10.22.195.3:57600'}], '10.22.196.3': [{'DBClientID': 'fb700431d91769c5c63d5f380a71085fac914b8f', 'ClientType': 'local_scheduler', 'Deleted': False, 'LocalSchedulerSocketName': '/tmp/scheduler78187679', 'GPU': 0.0, 'CPU': 8.0, 'mujoco': 15.0, 'AuxAddress': '10.22.196.3:49323'}, {'DBClientID': '13da60a13c5bf2238296df0d953938c6c39073b6', 'ClientType': 'plasma_manager', 'Deleted': False, 'store_socket_name': '/tmp/plasma_store78738634', 'manager_socket_name': '/tmp/plasma_manager24412265', 'AuxAddress': '10.22.196.3:49323'}]}

    # if compact is True, always delegate to builtin pprint module
    nl.pprint(data, width=300, compact=True)
    nl.pprint(data, width=300, indent=4)


def test_ppfmt():
    d1 = {'a': {'a': {'a': {'a': {'a': {'b': 10}}}}}}
    d2 = {'A': {'A': {'A': {'A': {'A': {'B': 10}}}}}}

    nl.ppf('D2->{2}, num={1:.3f}, D1->{0}',
           d1, 1/7, d2,
           width=10, depth=4, compact=False)
    nl.ppf('compact D2->{2}, num={1:.3f}, D1->{0}',
           d1, 1/7, d2,
           width=10, depth=3, compact=True)
    nl.ppf('{myd2} myerr {myd2}', myd2=d2, width=35)
