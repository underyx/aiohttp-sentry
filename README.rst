aiohttp-sentry
==============

.. image:: https://circleci.com/gh/underyx/aiohttp-sentry.svg?style=shield
   :target: https://circleci.com/gh/underyx/aiohttp-sentry
   :alt: CI Status

An aiohttp_ middleware for reporting errors to Sentry_. Python 3.5+ is required.

Usage
-----

Just add ``SentryMiddleware`` as a middleware:

.. code-block:: python

    from aiohttp import web
    from aiohttp_sentry import SentryMiddleware
    app = web.Application(middlewares=[SentryMiddleware()])

If you want to customize error reporting,
you can use the optional ``sentry_kwargs`` parameter,
which is a ``dict`` of kwargs passed to the lower-level Sentry library, ``raven``.
With this, you can specify environment details, filter out specific exceptions, and so on:

.. code-block:: python

    from aiohttp import web
    from aiohttp_sentry import SentryMiddleware
    app = web.Application(
        middlewares=(
            SentryMiddleware({
                'environment': 'foo',
                'release': 'bar',
                'ignore_exceptions': 'aiohttp.HTTPClientError'
            }),
            # ...
        ),
    )

.. _aiohttp: http://aiohttp.readthedocs.io/en/stable/
.. _Sentry: http://sentry.io/
