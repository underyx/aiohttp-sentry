# CHANGELOG

## 0.6.0 (2019-07-11)

- Add option to patch stdlib logging to send events (thanks, @Natim!)

## 0.5.0 (2019-01-10)

- Use new-style, aiohttp 2.3+ middleware definition,
  to get rid of the warning aiohttp emits about this
- Install a modified `sys.excepthook` which closes the Sentry transport
- Check if a protocol exists before trying to access the scheme
- Format the codebase with Black
- Bump requirements to raven 6.10

## 0.4.1 (2018-07-23)

- Fix stucture of how `REMOTE_ADDR` is passed, to get rid of this error on Sentry:
  > Discarded invalid parameter 'env'

## 0.4.0.post1 (2018-07-23)

- Un-bump requirements to raven 6.9, as 6.10 has not been released yet :see_no_evil:

## 0.4.0 (2018-07-23)

- Allow adding custom extra data to be passed with exception info (thanks, @playpauseandstop!)
- Pass HTTP scheme with events by default (thanks for this too, @playpauseandstop!)
- Fix an error when no transport is available (thanks, @o3o3o!)
- Bump requirements to raven 6.10

## 0.3.0 (2018-04-25)

- Bump requirements to raven 6.7 and raven-aiohttp 0.7.x

## 0.2.0 (2017-08-28)

- Bump requirements to raven 6.x and raven-aiohttp 0.5.x

## 0.1.0 (2016-12-16)

- Initial release
