nanolog
=======

Life is too short. Use ``nanolog`` to make logging and printing simpler!

``nanolog`` features a convenient logger API built on top of python's
builtin ``logging``.

The library also ships with many printing utilities. Python 3 only.

Installation
------------

From stable package on PyPI

.. code:: bash

    pip install nanolog

From bleeding edge master branch

.. code:: bash

    pip install git+git://github.com/SurrealAI/nanolog.git

nanolog.Logger
==============

Logging levels, from least severe to most:

-  ``LOG_ALL``: log everything
-  ``TRACE``: fine-grained debugging messages
-  ``DEBUG``: normal debugging
-  ``INFO``: messages you usually don't want to see
-  ``NOTICE`` (i.e. ``INFO5``): non-error messages you usually want to
   see
-  ``WARNING``: exceptional circumstances that might not be errors
-  ``ERROR``: errors that occur, but are anticipated and handled
-  ``CRITICAL``: fatal errors that lead to termination
-  ``LOG_OFF``: turn off all logging

.. code:: python

    import nanolog as nl

    logger = nl.Logger.create_logger(
        'main',
        stream='out',
        level='debug',
    )

    logger.info('my', 3, 'world', 1/16.)  # just like print
    # >>> my 3 world 0.0625

    # nanolog use 'warn' instead of 'warning'
    logger.warnfmt('{}, we are {:.3f} miles from {planet}',
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

Prettyprint support (uses the thirdparty lib ``prettyprinter``)

.. code:: python

    logger.infopp7(...)
    logger.warnppfmt('my warning {:.3f} format {:.2f} string', 1/7., 1/9.)

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

Convenient aliases (``pp`` stands for ``prettyprint``; a single ``p``
means normal print)

+--------------+--------------------+
| short        | original           |
+==============+====================+
| ``pf``       | ``printfmt``       |
+--------------+--------------------+
| ``pferr``    | ``printfmterr``    |
+--------------+--------------------+
| ``pstr``     | ``printstr``       |
+--------------+--------------------+
| ``perr``     | ``printerr``       |
+--------------+--------------------+
| ``pp``       | ``pprint``         |
+--------------+--------------------+
| ``ppstr``    | ``pprintstr``      |
+--------------+--------------------+
| ``ppf``      | ``pprintfmt``      |
+--------------+--------------------+
| ``ppfstr``   | ``pprintfmtstr``   |
+--------------+--------------------+

TODO: talk about global configs

Print redirection context managers
----------------------------------

-  PrintRedirection
-  PrintFile
-  PrintSuppress
-  PrintString
