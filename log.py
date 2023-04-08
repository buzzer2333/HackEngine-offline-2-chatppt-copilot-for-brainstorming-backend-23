import logging

logging.basicConfig(level=logging.INFO)


class Log:
    @classmethod
    def infof(cls, format, *args):
        msg = format % args
        logging.info(msg)
