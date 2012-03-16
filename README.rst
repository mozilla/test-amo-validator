Functional / regression test suite for `amo-validator`_, the Add-on validator
used at http://addons.mozilla.org/

Install
=======

You need Python 2.6 or higher.  Then clone this repo::

  git clone git://github.com/mozilla/test-amo-validator.git

Install the dependencies::

  cd test-amo-validator
  pip install -r requirements.txt

You'll probably want to do all of this inside a virtualenv_ using
`virtualenvwrapper`_.

In addition to this command you also need to **build spidermonkey from
source** as detailed in `amo-validator`_'s install instructions.

Usage
=====

::

  cd test-amo-validator
  nosetests --processes=2

Then make a cup of tea while all of those tests run.  It takes a while.
If you have more than two cores on your machine or you don't mind pwnage,
you can try to increase the number of parallel processes used for testing.

The Validator
=============

By default, the HEAD of `amo-validator`_'s git repo will be installed.
If you want to run the tests against your local amo-validator, install it
like this within your test-amo-validator virtualenv::

  pushd ~/amo-validator
  python setup.py develop --no-deps
  popd

.. _`amo-validator`: https://github.com/mozilla/amo-validator
.. _`virtualenv`: http://pypi.python.org/pypi/virtualenv
.. _`virtualenvwrapper`: http://www.doughellmann.com/docs/virtualenvwrapper/