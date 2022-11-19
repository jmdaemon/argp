from argp.argp import Option, Command, Argp

from loguru import logger
import sys, os

def build_cli():
    ''' Creates the command line interface '''
    # TODO: Add flag option to disable capitlization of {prog} in program description
    PROGRAM_DESCRIPTION = '{prog} - Convert ASCII text to Unicode values'
    PROGRAM_USAGE = '{prog} [COMMAND...] [OPTIONS...] [text]'

    morse_options = [
        Option('-m', '--morse'  , help='Convert text to Morse code'),
        Option('-a', '--ascii'  , help='Convert text to ASCII text'),
    ]

    options = [
        # Commands
        Command('morse', morse_options, lambda x: x, help='Convert to and from ASCII and morse code'),
        # Global CLI Options
        Option('-v', '--version'        , help='Show program version'),
        Option('-V', '--verbose'        , help='Enable verbose mode'),
        # Format Options
        Option('-b' , '--bold'          , 'bold'            , help='Bold text'),
        Option('-i' , '--italic'        , 'italic'          , help='Italicized text'),
    ]

    argp = Argp(options, usage=PROGRAM_USAGE, desc=PROGRAM_DESCRIPTION)
    return argp

def create_logger():
    # Create the logger
    logger.remove() # Override default logger
    # Format: [2022-09-01 23:36:01.792] [DEBUG] [bin_name.main:150] Hello!
    PROGRAM_LOG_MSG_FORMAT = '\x1b[0m\x1b[32m[{time:YYYY-MM-DD HH:mm:ss.SSS}]\x1b[0m [<lvl>{level}</>] [<c>{name}:{line}</>] {message}'
    loglevel = 'ERROR' if os.environ.get('LOGLEVEL') is None else os.environ.get('LOGLEVEL')
    logger.add(sys.stdout, format=PROGRAM_LOG_MSG_FORMAT, level=loglevel)

def main():
    create_logger()

    # Test the command line interface

    # TODO: Think of a better way to store & handle arguments
    argp = build_cli()
    active_comps: list = argp.parse()

    # Arguments and the activated components
    args = argp.argp.args

    for argument in args:
        print(f'{argument=}')
