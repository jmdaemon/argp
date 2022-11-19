import typing, sys, inspect, os

# TODO:
    # - Only source of arguments is in the options list
    # Argp:
    # Priority
        # - Add subcommand options
        # - Add callbacks with arguments feature
        # - Add support for options with nargs, + specify strings for options
        #   - Create type option to specify arg type, and ensure that an arg value
        #       is given for it in ArgParser.parse()
    # - Flesh out rest of the support for subcommands
    # - Add support for parsing multiple options & text
    # - Move argp declaration to separate python module
    # - Write unit tests, documentation, create package, upload

HelpFormatter = typing.NewType("HelpFormatter", None)

# class OptionsFormatter():
    # ''' Formats command line options '''
    # def __init__(self, argp_args: list,
                 # format='{space:<{indent}}{short_flag:<{short_padding}}{long:<{long_padding}}{help}\n',
                 # indent=2, short_padding=6, long_padding=21, *args, **kwargs):
        # self.args = argp_args
        # self.format = format
        # self.indent = indent
        # self.format = format
        # self.short_padding = short_padding
        # self.long_padding = long_padding
        # self.msg = ''

    # def format_help(self):
        # for arg in self.args:
            # if isinstance(arg, Option):
                # # Default option format:
                # #   -v,  --version              Show program version
                # #   -sb, --sub                  Subscript text
                # self.msg += self.format.format(
                    # space=' ', indent=self.indent,
                    # short_padding=self.short_padding, long_padding=self.long_padding,
                    # short_flag=arg.short + ',', long=arg.long, help=arg.help)
        # return self.msg

# class HelpFormatter():
    # DEFAULT_HEADER_FORMAT: str = inspect.cleandoc(
        # '''
        # {usage_indicator}: {usage}
        # {desc}\n
        # {arg_defs}
        # ''')
    # DEFAULT_INDICATOR = 'Usage'

    # def __init__(self, arg_defs, prog='', usage='', desc='',
                 # options_formatter = None,
                 # usage_indicator=DEFAULT_INDICATOR, usage_format=DEFAULT_HEADER_FORMAT):
                 # # indent=2,
                 # # short_padding=6,
                 # # long_padding=21,
        # self.arg_defs = arg_defs
        # self.prog = prog
        # self.usage = usage
        # self.desc = desc
        # self.msg = ''

        # # Format
        # self.options_formatter = OptionsFormatter(arg_defs) if options_formatter is None else options_formatter
        # self.usage_indicator = usage_indicator
        # self.usage_format = usage_format

    # def format_help(self):
        # prog = self.prog
        # usage_indicator = self.usage_indicator
        # usage = self.usage
        # desc = self.desc

        # arg_defs = ''

        # # Copy usage_format, usage strings
        # usage_msg = self.usage[:]
        # desc_msg = self.desc[:]
        # msg = self.usage_format[:]

        # options_msg: str = ''
        # cmds_msg: str = ''

        # arg_def: Command | Option
        # # TODO: Ideal command default format
        # # Command Format:
        # # command-to-option:
        # # id                    help
        # #   short, long         help
        # #   short, long         help
        # # command-to-command:
        # # id        help
        # #   short, long         help
        # #   id        help
        # #       short, long         help

        # for arg_def in self.arg_defs:
            # # TODO: This solution only parses one layer of options for commands
            # # TODO: Ideally this would recursively parse all command options
            # if isinstance(arg_def, Command):
                # space = ' '
                # id = arg_def.id
                # help = arg_def.help

                # format = ''
                # format = f'{space:<2}{id:<27}{help}'
                # cmds_msg += format

                # cmd_options_msg = ''
                # # TODO: Refactor this
                # for cmd_arg_def in arg_def.args:
                    # if isinstance(cmd_arg_def, Option):
                        # space = ' '
                        # short = cmd_arg_def.short
                        # long = cmd_arg_def.long
                        # help = cmd_arg_def.help

                        # short_flag = short + ','
                        # # TODO: These should not be hardcoded
                        # format = f'{space:<4}{short_flag:<6}{long:<19}{help}\n'
                        # cmd_options_msg += format
                # cmds_msg +=  '\n' + cmd_options_msg + '\n'

        # options_msg += self.options_formatter.format_help()

        # logger.debug(f'{prog=} {desc=} {usage=}')
        # logger.debug(cmds_msg)
        # logger.debug(options_msg)

        # # Format the help message
        # usage_msg = usage_msg.format(prog=prog)
        # desc_msg = desc_msg.format(prog=prog.capitalize())

        # arg_defs = 'Commands\n' + cmds_msg + 'Options\n' + options_msg if cmds_msg != '' else options_msg
        # msg = msg.format(usage_indicator=usage_indicator, usage=usage_msg, desc=desc_msg, arg_defs=arg_defs)

        # msg = msg.rstrip() # Remove last newline
        # self.msg = msg

    # def show_usage(self):
        # self.format_help()
        # print(self.msg)
        # sys.exit(1)

