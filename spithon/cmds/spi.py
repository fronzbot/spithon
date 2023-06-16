"""SPI Commands."""
import click
from spithon.cmds.common import CONTEXT_SETTINGS, OPTS
from spithon.core import spi as spi_ctrl


@click.group()
def spi():
    """SPI command group."""
    pass


@spi.command(context_settings=CONTEXT_SETTINGS)
@click.argument("word", required=True)
@OPTS.add_opts(OPTS.rd_wr_opts)
def write(word, verbose, crc):
    """Write WORD over SPI.

    WORD can be an integer or hex string.
    """
    spi_ctrl.spi_write(word, crc=crc, verbose=verbose)


@spi.command(context_settings=CONTEXT_SETTINGS)
@click.argument("word", required=True)
@OPTS.add_opts(OPTS.rd_wr_opts)
def read(word, verbose, crc):
    """Send SPI read with WORD as data.

    WORD can be an integer or hex string.
    """
    click.echo(hex(spi_ctrl.spi_read(word, crc=crc, verbose=verbose)))


@spi.command(context_settings=CONTEXT_SETTINGS)
@click.argument("word", required=True)
def gen_crc(word):
    """Generate a CRC word from a data word.

    WORD can be an integer or hex string.
    """
    click.echo(hex(spi_ctrl.crc_val(word)))
