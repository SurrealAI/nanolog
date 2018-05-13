nanolog
=======

Life is too short. Use ``nanolog`` to make logging and printing simpler!

``nanolog`` features a convenient logger API built on top of python's
builtin ``logging``.

The library also ships with many printing utilities. Python 3 only.

Installation:

.. code:: bash

    pip install nanolog

nanolog.Logger
==============

.. code:: python

    import nanolog as nl

    logger = nl.Logger.get_logger(
        'main',
        stream='out',
        level='debug',
    )

    logger.info('my', 3, 'world', 1/16.)  # just like print
    # >>> my 3 world 0.0625

    logger.warningfmt('{}, we are {:.3f} miles from {planet}',
                      'Houston', 17/7, planet='Mars')  # just like str.format
    # >>> Houston, we are 2.429 miles from Mars

Use a trailing number to indicate level, the larger the higher priority

.. code:: python

    logger.info7(...)  # info level 7
    logger.errorfmt8(...)  # error level 8

Display a banner line or block

.. code:: python

    logger.infobanner3('my', 3, 'world', symbol='!', banner_len=16, banner_lines=3)

prints:

::

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!!!!!! my 3 world !!!!!!!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!

Of course, banner method also comes with a ``str.format`` version

.. code:: python

    logger.debugbannerfmt(
        '{3}&{0}&{2}&{1}', 'a', 'b', 'c', 'd', 
        symbol='<*_*>', banner_len=16, banner_lines=6
    )

displays:

::

    <*_*><*_*><*_*><*_*><*_*>
    <*_*><*_*><*_*><*_*><*_*>
    <*_*><*_ d&a&c&b <*_*><*_
    <*_*><*_*><*_*><*_*><*_*>
    <*_*><*_*><*_*><*_*><*_*>
    <*_*><*_*><*_*><*_*><*_*>

Logger config
-------------

TODO

Time formatting
---------------

TODO

Printing utililites
===================

prettyprint
-----------

Better alternatives for the ``pprint`` module in python standard lib.

-  ``pprint``: takes variable number of objects, just like ``print()``

-  ``pprintstr``: return string instead of printing to IO stream

-  ``pprintfmt``: just like ``print('...'.format)``

-  ``pprintfmtstr``: return string instead of printing to IO stream

Convenient aliases:

+--------------------+------------+
| original           | short      |
+====================+============+
| ``pprint``         | ``pp``     |
+--------------------+------------+
| ``pprintstr``      | ``pps``    |
+--------------------+------------+
| ``pprintfmt``      | ``ppf``    |
+--------------------+------------+
| ``pprintfmtstr``   | ``ppfs``   |
+--------------------+------------+

TODO: talk about global configs

Print redirection context managers
----------------------------------

-  PrintRedirection
-  PrintFile
-  PrintSuppress
-  PrintString
