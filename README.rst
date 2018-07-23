##############
aiohttp-sentry
##############

.. image:: https://circleci.com/gh/underyx/aiohttp-sentry.svg?style=shield
   :target: https://circleci.com/gh/underyx/aiohttp-sentry
   :alt: CI Status

An aiohttp_ middleware for reporting errors to Sentry_. Python 3.5+ is required.

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
                **super().get_extra_data(request)
                'settings': request.app['settings'],
            }

While ``get_extra_data`` is a coroutine,
which means it can make database queries, API calls,
or other I/O operations, use this carefully!
Make sure you understand the implications of executing expensive operations every time an error happens.
If the root cause of the error is an overloaded database,
you are just going to make the problem worse,
while not even being able to get the extra info you wanted.
