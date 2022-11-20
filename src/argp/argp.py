import typing, sys, inspect, os
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

class Option():
    def __init__(self, short: str, long: str, id:str = '', val: typing.Any = None, flag = False,
                 cb: typing.Callable = None, help='', *args, **kwargs):
        self.argids = ArgID(self, [short, long, id])
        self.flag = flag
        self.val = val
        self.cb = cb
        self.help = help

    def get_comp(self, id: str):
        return self.argids.get_comp(id)

    def is_flag(self):
        return True if self.flag else False

class Command():
    ''' Contains sub options '''
    def __init__(self, id='', cli_defs: list = [],
                 cb: typing.Callable = None, help='', *args, **kwargs):
        self.cli_defs = cli_defs
        self.argids = ArgID(self, [id])
        self.args = []
        self.cb = cb
        self.help = help

# class StrictCommand(Command):
    # def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)

class ArgID():
    ''' Maps many ids to a single common ArgInterfaceComponent

    Allows you to retrieve an Option/Command definition using either the shortname, longname, or command id
    '''
    def __init__(self, comp: Command | Option, comp_ids=[]):
        self.comp_ids = comp_ids
        self.comp = comp
        self.comp_map: dict[str, Command | Option] = {}

        # Populate the comp_map with the various ids
        for comp_id in self.comp_ids:
            self.comp_map[comp_id] = self.comp

    def get_comp(self, id: str):
        return self.comp_map[id]

# Flattens the ids of options, commands into a single dict
class ArgsMap():
    def __init__(self, cli_defs: list):
        self.all_comp_ids = []
        self.all_comp_maps = {}
        # self.raw_args = []
        self.args = []

        # Flatten all the ids into a single dict mapping
        cli_def: Command | Option
        for cli_def in cli_defs:
            comp_map = cli_def.argids.comp_map
            for id, comp in comp_map.items():
                self.all_comp_ids.append(id)
                self.all_comp_maps[id] = comp

    def get_comp(self, id: str):
        res = None if not self.all_comp_maps.__contains__(id) else self.all_comp_maps[id]
        return res

def argp_parse(argp: ArgsMap, argvs: list):
    ''' Parses the given command line arguments and returns a list of the active cli components '''
    logger.debug('Parsing arguments')
    active_comps = []

    index = 0
    for argv in argvs:
        logger.debug(f'Argument #{index + 1}: {argv}')
        arg: Command | Option | None = argp.get_comp(argv)

        logger.debug(f'Type: {type(arg)}')
        logger.debug(f'{arg=}')

        if isinstance(arg, Command):
            nested_argmap = ArgsMap(arg.cli_defs)
            active_comps += argp_parse(nested_argmap, argvs[index:])

        elif isinstance(arg, Option):
            arg.val = True if arg.is_flag() else arg.val

        if arg != None:
            active_comps.append(arg)
            if arg.cb != None:
                arg.cb()
        else:
            argp.args += argv
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
        self.argp = ArgsMap(cli_defs)

        # Create HelpFormatter if not already made
        # if help_formatter == None:
            # self.help = HelpFormatter(arg_defs=cli_defs, prog=os.path.basename(sys.argv[0]), usage=usage, desc=desc)
            # help_option = Option('-h', '--help', cb=self.help.show_usage, help='Show program usage')
            # cli_defs.append(help_option)

        self.raw_args = sys.argv[1:]
        self.desc = desc

    def parse(self):
        return argp_parse(self.argp, self.raw_args)

