The librtree-python package
===========================

*Note: This code is in development: While the build and query
code is implemented, it is only lightly tested*

A Python native extension implementing the R-tree spatial
index of Guttman-Green.  The code is an embedded version of
`librtree <http://soliton.vm.bytemark.co.uk/pub/jjg/en/code/librtree/>`_.


Dependencies
------------

Just `Jansson <http://www.digip.org/jansson/>`_: this common library
may be in your operating-system's repositories. On Debian, Ubuntu and
derivatives:

.. code-block:: sh

   apt-get install libjansson-dev

On RedHat, CentOS:

.. code-block:: sh

    yum install jansson-devel

On OSX:

.. code-block:: sh

    brew install jansson

One does not need to install `librtree` itself, the library-code is
embedded within the package.
