"""Module for all SPI related functionality."""
import click
import crc as crc_calc
from spithon.core import conv_to_int
from spithon.core.config import SPI_VALID, SpiInterface, CRCHandler

SPI_IF = SpiInterface(device="RPi.SPI")
CRC_CFG = CRCHandler(device="RPi.CRC")


def int_to_bytes(word, length=4, crc=False):
    """Convert int to array of byte ints."""
    word_bytes = bytearray(word.to_bytes(length, "big"))
    if crc:
        crc_word = crc_val(word).to_bytes(CRC_CFG.num_bytes, "big")
        word_bytes.extend(crc_word)
    int_bytes = []
    for byte in word_bytes:
        int_bytes.append(byte)
    return int_bytes


def spi_write(word, crc=False, verbose=False):
    """Write address over SPI."""
    word = conv_to_int(word)
    int_bytes = int_to_bytes(word, length=SPI_IF.num_bytes, crc=crc)
    wr_word = int.from_bytes(int_bytes, "big")
    click.secho(f"INFO: Sending {hex(wr_word)}", fg="magenta")
    if SPI_VALID:
        SPI_IF.spi_if.xfer(int_bytes)
    return wr_word


def spi_read(word, crc=False, verbose=False):
    """Read address over SPI."""
    word = conv_to_int(word)
    int_bytes = int_to_bytes(word, length=SPI_IF.num_bytes)
    if crc:
        int_bytes.extend([0 for x in range(0, int(CRC_CFG.width / 8))])
    tx_word = int.from_bytes(int_bytes, "big")
    if verbose:
        click.secho(f"INFO: Sending {hex(tx_word)}", fg="magenta")
    if not SPI_VALID:
        return tx_word
    read_val = SPI_IF.spi_if.xfer(int_bytes)
    read_val = int.from_bytes(read_val, "big")
    if verbose:
        click.secho(f"INFO: Received {hex(read_val)}", fg="magenta")
    full_word = tx_word | read_val
    if crc:
        crc_word = full_word & (2**CRC_CFG.width - 1)
        check_crc((full_word >> CRC_CFG.width), crc_word, verbose=verbose)
        if verbose:
            click.secho(f"INFO: Extracted CRC word {hex(crc_word)}", fg="magenta")
    return full_word


def check_crc(word, crc_word, verbose=False):
    """Check expected CRC."""
    crc_exp = crc_val(word)
    if crc_word != crc_exp:
        if verbose:
            click.secho(f"CRC ERROR: Expected {hex(crc_exp)}", fg="red")
        return False
    return True


def crc_val(word):
    """Calculate CRC value."""
    word = conv_to_int(word)
    crc_config = crc_calc.Configuration(
        width=CRC_CFG.width,
        polynomial=CRC_CFG.poly,
        init_value=CRC_CFG.initial,
        reverse_input=False,
        reverse_output=False,
    )
    calculator = crc_calc.Calculator(crc_config)
    return calculator.checksum(word.to_bytes(SPI_IF.num_bytes, byteorder="big"))
