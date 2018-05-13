DEBUG = 10
DEBUG1 = 11
DEBUG2 = 12
DEBUG3 = 13
DEBUG4 = 14
DEBUG5 = 15
DEBUG6 = 16
DEBUG7 = 17
DEBUG8 = 18
DEBUG9 = 19
INFO = 20
INFO1 = 21
INFO2 = 22
INFO3 = 23
INFO4 = 24
INFO5 = 25
INFO6 = 26
INFO7 = 27
INFO8 = 28
INFO9 = 29
WARNING = 30
WARNING1 = 31
WARNING2 = 32
WARNING3 = 33
WARNING4 = 34
WARNING5 = 35
WARNING6 = 36
WARNING7 = 37
WARNING8 = 38
WARNING9 = 39
ERROR = 40
ERROR1 = 41
ERROR2 = 42
ERROR3 = 43
ERROR4 = 44
ERROR5 = 45
ERROR6 = 46
ERROR7 = 47
ERROR8 = 48
ERROR9 = 49
CRITICAL = 50
CRITICAL1 = 51
CRITICAL2 = 52
CRITICAL3 = 53
CRITICAL4 = 54
CRITICAL5 = 55
CRITICAL6 = 56
CRITICAL7 = 57
CRITICAL8 = 58
CRITICAL9 = 59


if __name__ == '__main__':
    from nanolog.logger import _LEVEL_MAPPING
    # generate this file
    for value, name in sorted(_LEVEL_MAPPING.items()):
        print('{} = {}'.format(name, value))

