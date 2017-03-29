import logging
import sys

from eleanorrigbot import start_listening

if __name__ == '__main__':
    logging.basicConfig(
        datefmt='%Y/%m/%d %H.%M.%S',
        format='%(levelname)s:%(name)s:%(message)s',
        level=logging.DEBUG,
        stream=sys.stdout,
    )

    start_listening()
