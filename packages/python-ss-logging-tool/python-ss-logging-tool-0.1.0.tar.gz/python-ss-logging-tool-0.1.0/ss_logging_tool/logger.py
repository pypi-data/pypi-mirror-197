from typing import Callable

from pino import pino
import nanoid
import traceback


class Logger:
    def __init__(self, logger: pino):
        self.logger = logger

    @staticmethod
    def create(app_name: str):
        logger = pino(
            bindings={"apptype": app_name, "metas": "main"}
        )
        return Logger(logger)

    def child(self, metas: dict = None):
        metas = metas or {}
        if 'request_id' not in metas:
            metas['request_id'] = nanoid.generate(size=10)
        return Logger(self.logger.child(metas=metas))

    def _call(self, method: Callable, *args, **kwargs):
        try:
            if args[0] and isinstance(args[0], dict):
                return method(dict(data=args[0]), *args[1:], **kwargs)
            else:
                return method(*args, **kwargs)
        except Exception as e:
            self.logger.warn('logger seems to have error')
            print(*args)

    def info(self, *args, **kwargs):
        self._call(self.logger.info, *args, **kwargs)

    def error(self, *args, **kwargs):
        # check if args[0] is an error type
        if args[0] and isinstance(args[0], Exception):
            tb = traceback.format_exc()
            self._call(self.logger.error, dict(traceback=tb), *args[1:], **kwargs)
        else:
            self._call(self.logger.error, *args, **kwargs)

    def debug(self, *args, **kwargs):
        self._call(self.logger.debug, *args, **kwargs)

    def warn(self, *args, **kwargs):
        self._call(self.logger.warn, *args, **kwargs)
