

Open Product API Client (for Django)
==============================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/open-product-api-client
:Keywords: Open Product API, Client, Django
:PythonVersion: 3.9

|build-status|
Currently compatible with Open Product 1.0.0

|python-versions| |django-versions| |pypi-version|

About
=====

Easily integrate `Open Product API`_ in your Django application. It currently only supports a few major endpoints such as get products, get producttypes, get themes and get organizations.

Installation
============

Requirements
------------

* Python 3.9 or newer
* Django 3.2 or newer


Install
-------

You can the install Open Product API Client either via the Python Package Index (PyPI) or 
from source.

To install using ``pip``:

.. code-block:: bash

    pip install open-product-api-client


Usage
=====

To use this with your project you need to follow these steps:

#. Add ``openproductapiclient`` to ``INSTALLED_APPS`` in your Django project's 
   ``settings.py``:

   .. code-block:: python

      INSTALLED_APPS = (
          # ...,
          "openproductapiclient",
      )


#. Configure your Open Product API connection and settings in the admin, under 
   **Open Product API client configuration**.

#. Done.


Licence
=======

Copyright © `Maykin Media B.V.`_, 2023

Licensed under the `MIT`_.

.. _`Maykin Media B.V.`: https://www.maykinmedia.nl
.. _`MIT`: LICENSE
.. _`Open Product API`: https://github.com/maykinmedia/open-product

.. |build-status| image:: https://github.com/maykinmedia/open-product-api-client/workflows/Run%20CI/badge.svg
    :alt: Build status
    :target: https://github.com/maykinmedia/open-product-api-client/actions?query=workflow%3A%22Run+CI%22
