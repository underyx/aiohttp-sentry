aiohttp-sentry
==============

.. image:: https://circleci.com/gh/underyx/aiohttp-sentry.svg?style=shield
   :target: https://circleci.com/gh/underyx/aiohttp-sentry
   :alt: CI Status

An aiohttp_ middleware for reporting errors to Sentry_. Python 3.5+ is required.

Usage
-----

``SentryMiddleware`` has optional ``sentry_kwargs`` parameter, which is
a ``dict`` of kwargs passed to ``Raven`` internally. That way you can specify
environment details, filter out specific types of exceptions, etc:

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
