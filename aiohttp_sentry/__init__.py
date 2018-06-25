from functools import partial

import raven
import raven_aiohttp


class SentryMiddleware:

    def __init__(self, sentry_kwargs=None):
        if sentry_kwargs is None:
            sentry_kwargs = {}

        sentry_kwargs = {
            'transport': raven_aiohttp.AioHttpTransport,
            **sentry_kwargs,
        }
        sentry_kwargs.setdefault('enable_breadcrumbs', False)
        self.client = raven.Client(**sentry_kwargs)

    async def __call__(self, app, handler):
        return partial(self.middleware, handler)

    async def middleware(self, handler, request):
        try:
            return await handler(request)
        except:
            self.client.captureException(data={
                'request': {
                    'query_string': request.query_string,
                    'cookies': request.headers.get('Cookie', ''),
                    'headers':  dict(request.headers),
                    'url': request.path,
                    'method': request.method,
                    'env': {
                        'REMOTE_ADDR': request.transport.get_extra_info('peername')[0],
                    }
                }
            })
            raise
