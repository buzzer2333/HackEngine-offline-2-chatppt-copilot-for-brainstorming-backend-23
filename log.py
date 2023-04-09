import logging

logging.basicConfig(level=logging.INFO)


class Log:
    @classmethod
    def infof(cls, fmt, *args):
        msg = fmt % args
        logging.info(msg)

    @classmethod
    def errorf(cls, fmt, *args):
        msg = fmt % args
        logging.error(msg)
