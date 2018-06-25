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

Advanced Usage
--------------

By default, `aiohttp-sentry` passes next data set to Sentry about failed
request,

- ``method``
- ``scheme``
- ``url``
- ``query_string``
- ``headers``
- ``cookies``
- ``env``

and in most cases this is just fine. However if you need more detailed reports
you can do it by overloading ``get_request_data`` method,

.. code-block:: python

    class DetailedSentryMiddleware(SentryMiddleware):

        def get_request_data(self, request):
            return {
                'settings': request.app['settings'],
                **super().get_request_data(request)
            }

You also able as well to pass more env data by overriding
``get_request_env_data`` method.

And when you need to add extra data to the Sentry you able to do it by
overriding ``get_extra_data`` coroutine method,

.. code-block:: python

    from aiohttp_session import get_session


    class DetailedSentryMiddleware(SentryMiddleware):

        async def get_extra_data(self, request):
            session = await get_session(request)
            return {
                'non_sensitive_data': session['non_sensitive_data'],
            }

As ``get_extra_data`` is a coroutine, you in theory be able to make a database
query or other async I/O operation, which is still not recommended.
