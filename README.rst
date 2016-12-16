aiohttp-sentry
==============

.. image:: https://circleci.com/gh/underyx/aiohttp-sentry.svg?style=shield
   :target: https://circleci.com/gh/underyx/aiohttp-sentry
   :alt: CI Status

An aiohttp_ middleware for reporting errors to Sentry_. Python 3.5+ is required.

Usage
-----

.. code-block:: python

    from aiohttp import web
    from aiohttp_sentry import SentryMiddleware
    app = web.Application(
        middlewares=(
            SentryMiddleware({
                'environment': 'foo',
                'release': 'bar',
            }),
            # ...
        ),
    )

.. _aiohttp: http://aiohttp.readthedocs.io/en/stable/
.. _Sentry: http://sentry.io/
