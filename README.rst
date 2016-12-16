aiohttp-sentry
==============

An aiohttp_ middleware for reporting errors to Sentry_. Python 3.5+ is required.

Usage
-----

.. code-block:: python

    from aiohttp import web
    from aiohttp_sentry import SentryMiddleware
    app = web.Application(
        middlewares=(
            SentryMiddleware,
            # ...
        ),
    )

.. _aiohttp: http://aiohttp.readthedocs.io/en/stable/
.. _Sentry: http://sentry.io/
