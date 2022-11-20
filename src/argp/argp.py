import typing, sys, inspect, os, collections
from collections.abc import MutableMapping
from collections import ChainMap
from loguru import logger

# Usage:
# 1. Declare options & interface ahead of time
# 2. Design the interface how you want (enable/disable strict type checking, help message formatting, etc)
# 3. Parse options on command line
# 4. Retrieve all arguments, index into dictionary create 

# Ideas (TODO):
# Options:
# 'dest' used to store values given to options
# 'id' used to rename the dest arg in args['dest'] 
# Options can be turned into 'flags'.
# Options can be activated by their short or long names
#
# General:
# Any commands/options that were activated should go into a dictionary returned by parse.
# Commands can only contain options for the forseeable moment.
#
# Positional Command (Splice):
# When invoked, options are checked until an unknown option type is found, or none are left
# this splits the argv into a splice that is assigned to the positional command.
#
# Strict Command (Subtractive):
# Treated as a completely separate parser that cannot detect global options
#
# Sub Command (Additive):
# Reads global options as well as its own options
#
# Callbacks
# - Lambda expressions, function objects or partials may be used.
# - Can accept arguments

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

    # cli_defs_flat_list = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)

    # flat_cli_defs = {}
    # map(lambda dictionary: flat_cli_defs.update(dictionary), [flatten_dict(cli_def.argids, '','') for cli_def in cli_defs])
    # return flat_cli_defs

    return dict(ChainMap(*[flatten_dict(cli_def.argids, '','') for cli_def in cli_defs]))

    # concat_dict = lambda dictionary: flat_cli_defs.update(dictionary)

    # cli_defs_flat_list = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)

    # cli_defs_flat_list = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)

    # flat_cli_defs = {}

    # Better
    # for cli_def in cli_defs:
        # argids: dict = cli_def.argids
        # flat_cli_defs.update({ key:arg for key,arg in argids.items() })
    # return flat_cli_defs

    # One liner
    # asdf = lambda cli_def: flatten_dict(cli_def.argids, '','')
    # flat_cli_defs = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)
    # return flat_cli_defs

    # flat_cli_defs = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)
    # return flat_cli_defs
    # flat_cli_defs = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)

    # return dict(map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs))

    # cli_defs_flat_list = map(lambda cli_def: flatten_dict(cli_def.argids, '',''), cli_defs)

    # return dict()

        # flat_cli_defs + dict()
        # [ flat_cli_defs [key]
            # argids.items()


        # comp_map = cli_def .argids
        # for id, comp in comp_map.items():
            # self.all_comp_ids.append(id)
            # self.all_comp_maps[id] = comp

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
    ''' Highly customizeable cli arguments parser

        This argument parsing library was created to address flaws in argparse,
        and direct parsing from sys.argv.

        Some gripes that I've found when using argparse are:
            - Usage and other docstring names aren't capitalized, and are unable to be modified.
            - Does not accept '-' or '--' as valid arguments (arguments will be "unknown" and will show the usage message)
            - Only one subcommand/callback can be executed

        When doing direct custom parsing from sys.argv:
            - Lots of tedious work to check inputs
            - No help/usage string by default
            - Awkward inputs & input handling
            - Specific to your project/no code reuse between programs

    '''

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

