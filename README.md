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

# Features

Usage:
    1. Declare options & interface ahead of time
    2. Design the interface how you want (enable/disable strict type checking, help message formatting, etc)
    3. Parse options on command line
    4. Retrieve all arguments, index into dictionary for variables

Ideas (TODO):
Options:
- [ ] 'dest' used to store values given to options
- [ ] 'id' used to rename the dest arg in args['dest']
- [ ] Options can be turned into 'flags'.
- [ ] Options can be activated by their short or long names

General:
- [ ] Any commands/options that were activated should go into a dictionary returned by parse.
- [ ] Commands can only contain options for the forseeable moment.

Positional Command (Splice):
- [ ] When invoked, options are checked until an unknown option type is found, or none are left
- [ ] this splits the argv into a splice that is assigned to the positional command.

Strict Command (Subtractive):
- [ ] Treated as a completely separate parser that cannot detect global options

Sub Command (Additive):
- [ ] Reads global options as well as its own options

Callbacks
- [ ] Lambda expressions, function objects or partials may be used.
- [ ] Can accept arguments

Forward Declarations of Types
