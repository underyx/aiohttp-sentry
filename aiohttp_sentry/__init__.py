import asyncio
from functools import partial
import sys

import raven
import raven_aiohttp


class SentryMiddleware:

    def __init__(self, sentry_kwargs=None, *, install_excepthook=True, loop=None):
        if sentry_kwargs is None:
            sentry_kwargs = {}

        sentry_kwargs = {
            'transport': raven_aiohttp.AioHttpTransport,
            'enable_breadcrumbs': False,
            # by default, do not let raven.Client install its own excepthook
            'install_sys_hook': not install_excepthook,
            **sentry_kwargs,
        }
        self.client = raven.Client(**sentry_kwargs)

        if install_excepthook:
            self.update_excepthook(loop)

    def update_excepthook(self, loop=None):
        """Update sys.excepthook so that it closes the Sentry transport.

        If a custom event loop is provided,
        it will be used for closing the Sentry transport
        derived from raven_aiohttp.AioHttpTransportBase
        instead of the event loop for the current context
        defined by the current event loop policy.
        """
        original_excepthook = sys.excepthook

        def aiohttp_transport_excepthook(*exc_info):
            """An aiohttp-transport-friendly excepthook.

            It closes the transport, which delivers the messages."""
            self.client.captureException(exc_info=exc_info, level='fatal')
            transport = self.client.remote.get_transport()
            if isinstance(transport, raven_aiohttp.AioHttpTransportBase):
                if loop is None:
                    loop = asyncio.get_event_loop()
                # wait for Sentry transport to send the outstanding messages
                loop.run_until_complete(transport.close())
            original_excepthook(*exc_info)

        sys.excepthook = aiohttp_transport_excepthook

    async def __call__(self, app, handler):
        return partial(self.middleware, handler)

    async def middleware(self, handler, request):
        try:
            return await handler(request)
        except:
            extra_data = await self.get_extra_data(request)
            self.client.captureException(data=extra_data)
            raise

    async def get_extra_data(self, request):
        data = {
            'request': {
                'query_string': request.query_string,
                'cookies': request.headers.get('Cookie', ''),
                'headers':  dict(request.headers),
                'url': request.path,
                'method': request.method,
                'scheme': request.scheme,
            },
        }

        if request.transport:
            data['request']['env'] = {'REMOTE_ADDR': request.transport.get_extra_info('peername')[0]}

        return data
