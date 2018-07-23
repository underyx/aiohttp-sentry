from functools import partial

import raven
import raven_aiohttp


class SentryMiddleware:

    def __init__(self, sentry_kwargs=None):
        if sentry_kwargs is None:
            sentry_kwargs = {}

        sentry_kwargs = {
            'transport': raven_aiohttp.AioHttpTransport,
            'enable_breadcrumbs': False,
            **sentry_kwargs,
        }
        self.client = raven.Client(**sentry_kwargs)

    async def __call__(self, app, handler):
        return partial(self.middleware, handler)

    async def middleware(self, handler, request):
        try:
            return await handler(request)
        except:
            extra_data = await self.get_extra_data(request)
            self.client.captureException(data={
                'request': await self.get_request_data(request),
                **extra_data
            })
            raise

    async def get_extra_data(self, request):
        return {}

    def get_request_data(self, request):
        return {
            'query_string': request.query_string,
            'cookies': request.headers.get('Cookie', ''),
            'headers':  dict(request.headers),
            'url': request.path,
            'method': request.method,
            'scheme': request.scheme,
            'env': self.get_request_env_data(request),
        }

    def get_request_env_data(self, request):
        return {
            'REMOTE_ADDR': request.transport.get_extra_info('peername')[0],
        }
