"""Main CLI function."""
import click
from spithon import __version__, PROJECT_DESCRIPTION
from spithon.cmds.spi import spi
from spithon.cmds.gpio import gpio
from spithon.cmds.benchmark import benchmark
from spithon.core import spi as _spi


HELP_STRING = f"spithon {__version__}\n\n{PROJECT_DESCRIPTION}"


@click.group()
def top():
    """CLI for Raspberry Pi SPI/GPIO Communication."""


# All top level commands go here
TOP_LEVEL_CMDS = [
    top,
    spi,
]

# All sub-commands go here
SUB_CMDS = [
    gpio,
    benchmark,
]

# Now create the CLI
for group in SUB_CMDS:
    top.add_command(group)

cli = click.CommandCollection(sources=TOP_LEVEL_CMDS, help=HELP_STRING)


@cli.result_callback()
def close_spi(result, **kwargs):
    """Close the SPI Interface."""
    if _spi.SPI_VALID:
        _spi.SPI_IF.spi_if.close()


if __name__ == "__main__":
    cli()
