import typing, sys, inspect, os, collections
from collections.abc import MutableMapping
from collections import ChainMap
from loguru import logger

# Forward Declarations of Types
Option = typing.NewType("Option", None)
ArgParser = typing.NewType("ArgParser", None)
Command = typing.NewType("Command", ArgParser)
Argp = typing.NewType("Argp", ArgParser)

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

# def argp_parse(argp: ArgsMap, argvs: list):
def argp_parse(argp: Args, argvs: list):
    ''' Parses the given command line arguments and returns a list of the active cli components '''
    logger.debug('Parsing arguments')
    active_comps = []

    index = 0
    for argv in argvs:
        logger.debug(f'Argument #{index + 1}: {argv}')
        arg: Command | Option | None = argp.get_arg(argv)

        logger.debug(f'Type: {type(arg)}')
        logger.debug(f'{arg=}')

        if isinstance(arg, Command):
            nested_argmap = Args(arg.cli_defs)
            active_comps += argp_parse(nested_argmap, argvs[index:])

        elif isinstance(arg, Option):
            arg.val = True if arg.is_flag() else arg.val

        if arg != None:
            active_comps.append(arg)
            if arg.cb != None:
                arg.cb()
        else:
            # argp.args += argv
            argp.args[index] = argv
    index += 1
    return active_comps

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

