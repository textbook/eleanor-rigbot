#!/usr/bin/env python
"""Configure logging and start the process."""
import logging
import sys

from eleanorrigbot import parse_args, start_listening


if __name__ == '__main__':
    ARGS = parse_args(sys.argv[1:])

    logging.basicConfig(
        datefmt='%Y/%m/%d %H.%M.%S',
        format='%(levelname)s:%(name)s:%(message)s',
        level=ARGS.log_level,
        stream=sys.stdout,
    )

    start_listening(location=ARGS.location)
