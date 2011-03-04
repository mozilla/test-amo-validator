Functional / regression test suite for `amo-validator`_, the Add-on validator
used at http://addons.mozilla.org/

Install
=======

Clone this repo with *all* submodules::

  git clone --recursive git://github.com/kumar303/test-amo-validator.git

Usage
=====

Requires Python 2.6 or higher.

::

  cd test-amo-validator
  python run_tests.py

Then make a cup of tea while all of those tests run.  It takes a while.

Requirements
============

All requirements are available to you when you clone the repository.
These are the same exact libraries used in the master branch of `Zamboni`_
and `Zamboni-lib`_.

If you want to try out a newer validator, create a `virtualenv`_
and install it::

  pip install --no-deps -e git://github.com/mattbasta/amo-validator.git#egg=amo-validator

You can pass the ``--no-deps`` flag since you already have the dependencies
from `Zamboni-lib`_.

.. _`amo-validator`: https://github.com/mattbasta/amo-validator
.. _`Zamboni`: https://github.com/jbalogh/zamboni/
.. _`Zamboni-lib`: https://github.com/jbalogh/zamboni-lib/
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
