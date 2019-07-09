##############
aiohttp-sentry
##############

.. image:: https://circleci.com/gh/underyx/aiohttp-sentry.svg?style=shield
   :target: https://circleci.com/gh/underyx/aiohttp-sentry
   :alt: CI Status

An aiohttp_ server middleware for reporting failed requests to Sentry_

*****
Usage
*****

Just add ``SentryMiddleware`` as a middleware:

.. code-block:: python

    from aiohttp import web
    from aiohttp_sentry import SentryMiddleware
    app = web.Application(middlewares=[SentryMiddleware()])

Configuration
=============

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

If you are using the standard library's ``logging`` module,
we have a convenient parameter to patch it for you,
to have logger calls send events to Sentry automatically:

.. warning::
    This modifies your logging configuration globally
    when you instantiate the middleware.
    Even if you don't end up using the middleware instance for a request,
    all your logs will be sent to Sentry.

.. code-block:: python

    import logging
    from aiohttp import web
    from aiohttp_sentry import SentryMiddleware

    app = web.Application(
        middlewares=[SentryMiddleware(patch_logging=True, sentry_log_level=logging.WARNING)],
    )

.. _aiohttp: http://aiohttp.readthedocs.io/en/stable/
.. _Sentry: http://sentry.io/

Attaching Data to Events
========================

By default, `aiohttp-sentry` passes this data alongside reported exceptions:

- HTTP scheme
- HTTP method
- URL
- Query String
- Request Headers (including cookies)
- Requester's IP address

If you need more data in sentry,
you can do that by subclassing from ``SentryMiddleware``
and overriding the ``get_extra_data`` method,
which returns all the above by default.
Here's what that looks like:

.. code-block:: python

    class DetailedSentryMiddleware(SentryMiddleware):

        async def get_extra_data(self, request):
            return {
                **await super().get_extra_data(request),
                'settings': request.app['settings'],
            }

While ``get_extra_data`` is a coroutine,
which means it can make database queries, API calls,
or other I/O operations, use this carefully!
Make sure you understand the implications of executing expensive operations every time an error happens.
If the root cause of the error is an overloaded database,
you are just going to make the problem worse,
while not even being able to get the extra info you wanted.
