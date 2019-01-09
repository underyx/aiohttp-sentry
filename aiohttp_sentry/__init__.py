from aiohttp import web
import raven
import raven_aiohttp


@web.middleware
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

    async def __call__(self, request, handler):
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
            },
        }

        if request.transport:
            data['request']['env'] = {'REMOTE_ADDR': request.transport.get_extra_info('peername')[0]}
            data['request']['scheme'] = request.scheme

        return data
