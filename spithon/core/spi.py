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
    if not SPI_VALID:
        return
    if verbose:
        click.secho(f"INFO: Sending bytes {[hex(x) for x in int_bytes]}", fg="magenta")
    SPI_IF.spi_if.xfer(int_bytes)
    return


def spi_read(word, crc=False, verbose=False):
    """Read address over SPI."""
    if not SPI_VALID:
        return 0
    word = conv_to_int(word)
    int_bytes = int_to_bytes(word, length=SPI_IF.num_bytes, crc=crc)
    if verbose:
        click.secho(f"INFO: Sending bytes {[hex(x) for x in int_bytes]}", fg="magenta")
    value = SPI_IF.spi_if.xfer(int_bytes)
    value = int.from_bytes(value, "big")
    read_value = value
    if crc:
        crc_word = value & (2**CRC_CFG.width - 1)
        if verbose:
            click.secho(f"INFO: Got CRC word {hex(crc_word)}", fg="magenta")
        read_value = value >> CRC_CFG.width
        raw_word = word | value
        check_crc(raw_word, crc_word, verbose=verbose)
    if verbose:
        click.secho(f"INFO: Read back {hex(read_value)}", fg="magenta")
    return value


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
