"""Common CLI command options."""
import click

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}


class CommandOpts:
    """Class to instantiate common options."""

    def __init__(self):
        """Initialize options class."""
        self.rd_wr_opts = [
            self.verbose(),
            self.crc(),
        ]

    def generic(
        self, name, help_string, is_arg=False, is_req=False, is_flag=False, default=None
    ):
        """Create generic option."""
        if is_arg:
            return click.argument(name, required=is_req, metavar=f"<{help_string}>")
        return click.option(
            f"--{name}",
            f"-{name[0]}",
            default=default,
            is_flag=is_flag,
            required=is_req,
            help=help_string,
        )

    def verbose(self):
        """Create verbose option."""
        return self.generic(
            "verbose", "Echo command to stdout", is_flag=True, default=False
        )

    def crc(self):
        """Create CRC option."""
        return self.generic("crc", "Use CRC", is_flag=True, default=False)

    def add_opts(self, opts):
        """Add options for click."""

        def _add_options(func):
            for option in reversed(opts):
                func = option(func)
            return func

        return _add_options


OPTS = CommandOpts()
