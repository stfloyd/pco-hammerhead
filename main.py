#!/usr/bin/python3

import os
import sys
import errno
import json

import app
from app import settings, logging


# -----------------------------------------------------------------------------
# Application Definition

def main(argv):
    '''
    Main entry point into the program.
    '''

    # Get arguments and argument parser.
    (args, parser) = app.cli(argv)

    # Initialize logging and set verbosity level.
    logger = logging.get_logger(__name__)

    logger.debug(f'Program arguments: {argv}')
    # Check if any command arguments have been passed.
    if (len(argv) <= 1):
        # No arguments passed.
        logger.warning(f'No command arguments passed')
        #parser.print_help()
        #sys.exit(errno.EAGAIN)

    if args.list_configs:
        configs = settings.list_configs()
        print(configs)
        return os.EX_OK

    # Initialize our app.
    try:
        app.init(args)
    except Exception as e:
        logger.exception(e)
        logger.failure(f'App initialization failed: {e}')
        parser.print_help()
        return os.EX_SOFTWARE

    # Load application configuration.
    try:
        config = app.load_config(args)
    except Exception as e:
        logger.exception(e)
        logger.failure(f'App configuration failed: {e}')
        parser.print_help()
        return os.EX_CONFIG

    # Do something with config before running main app logic.

    # Run main app logic
    try:
        exit_code = app.process(args, config)
    except Exception as e:
        logger.exception(e)
        logger.failure(f'App processing failed: {e}')
        parser.print_help()
        return os.EX_SOFTWARE

    # Handle anything else you need to, we're getting out of here.

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
