# Argpy

Argpy is a command line interface designer library created as an alternative to argparse, and inspired by GNU's Argp.
Argpy (pronounced arg-pie) offers more freedom to customize and build your command line interface over other alternatives.
Argpy is also more lightweight than other solutions and provides more sane/desired defaults.

This argument parsing library was created to address flaws in `argparse`, and be a higher level of abstraction than direct parsing from `sys.argv`.

Some drawbacks to `argparse`:
    - Usage and other docstring names aren't capitalized, and are unable to be modified.
    - Does not accept '-' or '--' as valid arguments (arguments will be "unknown" and will show the usage message)
    - Only one subcommand/callback can be executed
    - Is not very flexible.

Meanwhile, directly parsing from `sys.argv` allows for more freedom but you also miss out on quality of life features such as:
    - Automatic default generated help/usage docstrings
    - Type checking
    - Subcommands, callbacks, and other features of most CLI libraries available by default.
    - Color
    - Config handling, flags, options, option arguments
    - Common code reuse between projects

## Usage

1. Declare options & interface ahead of time
2. Design the interface how you want (enable/disable strict type checking, help message formatting, etc)
3. Parse options given
4. Retrieve all arguments from the returned dictionar

## Features

Important features are starred.

Completed:
- [X] Option, Command and Argument CLI types
- [X] Options can be specified by their short or long names
- [X] Basic no parameter callbacks
- [X] All options/commands/arguments passed are stored into a dictionary returned by parse.

Work in Progress:
- [ ] \* More flexibility/modularity in `argp_parse` for custom command, option types
- [ ] \* More generator options to create certain options/commands automatically
- [ ] \* Global options to be shared/enabled across sub commands
- [ ] \* Argparse-like 'nargs' variable (but only accepts an int)
- [ ] \* Argparse-like 'type' var (Custom variable types for Options, Commands)
    - [ ] Opt-in type checking at runtime
- [ ] \* Argparse-like 'required' (Optional / Required options)

Help Formatting;
- [ ] \* Flat list help docstring listing all commands with their options
- [ ] \* Tree help docstring listing all commands without options
- [ ] \* -h, --help option specifies more specific help format message for commands
- [ ] \* Command specific help message formatting.

Optional:
- [ ] 'dest' used to store values given to options (can be referenced with args.dest)
- [ ] Alternative 'verbose' option that specifies levels of verbosity
- [ ] Debug flag in Argp to enable/disable logging of argument parsing

Options:
- [ ] \* 'id' used to rename the dest arg in args['dest']
- [ ] \* 'flag' to specify toggleable options with on/off values.

*Positional Command (Splice):*

When invoked, options are checked until an unknown option type is found, or none are left

- [ ] this splits the argv into a splice that is assigned to the positional command.

*Strict Command (Subtractive):*

When invoked, is treated as a completely separate parser from the main parser, that cannot detect global options.

*Sub Command (Additive):*

When invoked, reads global options in addition to its own options

*Callbacks:*

Provides a custom function with some specified arguments (or none at all),

to be invoked later when being parsed.
- [ ] Lambda expressions, function objects or partials may be used.
- [ ] Can accept arguments
