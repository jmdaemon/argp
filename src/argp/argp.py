import typing, sys
from collections.abc import MutableMapping
from collections import ChainMap
from loguru import logger

# Helper functions
def flatten_dict(d, parent_key='', sep='_'):
    ''' Flattens a nested dict into a flat dict '''
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def map_keys_to_dict(keys: list[str], value: typing.Any):
    ''' Map multiple keys to the same value in a dict '''
    return {key:value for key in keys}

def flatten_args(cli_defs: list):
    ''' Flatterns a list of cli ids and definitions into a dict '''
    return dict(ChainMap(*[flatten_dict(cli_def.argids, '','') for cli_def in cli_defs]))

class Option():
    def __init__(self, short: str, long: str, id:str = '', val: typing.Any = None, flag = False,
                 cb: typing.Callable = None, help='', *args, **kwargs):
        self.argids = map_keys_to_dict([short, long, id], self)
        self.flag = flag
        self.val = val
        self.cb = cb
        self.help = help

    def is_flag(self):
        return True if self.flag else False

class Command():
    ''' Contains sub options '''
    def __init__(self, id = '', cli_defs = [], cb: typing.Callable = None, help='', *args, **kwargs):
        self.cli_defs = cli_defs
        self.argids = map_keys_to_dict([id], self)
        self.args = []
        self.cb = cb
        self.help = help

class Args:
    def __init__(self, cli_defs: list):
        self.raw_args = []
        self.cli_defs: dict = flatten_args(cli_defs)
        self.args = {}

    def get_arg(self, id: str):
        return None if not self.cli_defs.__contains__(id) else self.cli_defs[id]

def argp_parse(argp: Args, argvs: list):
    ''' Parses the given command line arguments and returns a dict of the cli definitions & arguments if any '''
    logger.debug('Parsing arguments')

    index = 0
    for argv in argvs:
        logger.debug(f'Argument #{index + 1}: {argv}')
        arg: Command | Option | None = argp.get_arg(argv)

        logger.debug(f'Type: {type(arg)}')
        logger.debug(f'{arg=}')

        if isinstance(arg, Command):
            # TODO: Callbacks
            argp.args.update({argv: argp.cli_defs[argv]})

        elif isinstance(arg, Option):
            arg.val = True if arg.is_flag() else arg.val

        # TODO Callbacks
        # Allow for strict, positional, and sub commands
        # Strit, positional will be easy, and subcommands should use argp's cli_defs
        if arg != None:
            argp.args.update({argv: arg})
            if hasattr(arg, 'cb') and (arg.cb != None):
                # Pass arguments, this should be done in a better more generic way
                # Does not support positional 'nargs'
                arg.cb(argvs[index:])
        else:
            argp.args[index] = argv
        index += 1
    return argp.args

class Argp():
    def __init__(self, cli_defs: list, usage='', desc='', help_formatter=None):
        self.argp = Args(cli_defs)

        # Create HelpFormatter if not already made
        # if help_formatter == None:
            # self.help = HelpFormatter(arg_defs=cli_defs, prog=os.path.basename(sys.argv[0]), usage=usage, desc=desc)
            # help_option = Option('-h', '--help', cb=self.help.show_usage, help='Show program usage')
            # cli_defs.append(help_option)

        self.raw_args = sys.argv[1:]
        self.desc = desc

    def parse(self):
        return argp_parse(self.argp, self.raw_args)
