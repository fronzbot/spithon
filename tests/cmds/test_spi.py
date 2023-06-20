"""Module for spi command testing."""
from unittest import TestCase
from unittest.mock import patch
from click.testing import CliRunner
from .. import mock_spidev


with patch("spithon.core.config.load_cfg") as mock_cfg:
    mock_cfg.side_effect = [
        mock_spidev.CFG_MOCK["RPi.SPI"],
        mock_spidev.CFG_MOCK["RPi.CRC"],
    ]
    from spithon.cmds import spi  # pyline: disable=wrong-import-order


class TestSpiCmds(TestCase):
    """Class for SPI command testing."""

    def setUp(self):
        """Set up the test class."""
        self.runner = CliRunner()
        spi.spi_ctrl.SPI_VALID = True
        spi.spi_ctrl.SPI_IF.spi_if = mock_spidev.SpiDev()
        spi.spi_ctrl.SPI_IF.spi_if.num_bytes = 4
        spi.spi_ctrl.SPI_IF.spi_if.word_length = 32
        spi.spi_ctrl.CRC_CFG.width = 8
        spi.spi_ctrl.CRC_CFG.poly = int("0xA2", 16)

    def test_write_hex(self):
        """Test the write command."""
        self.runner.invoke(spi.write, ["0xDEADBEEF"])
        exp_bytes = [222, 173, 190, 239]
        self.assertListEqual(spi.spi_ctrl.SPI_IF.spi_if.tx_bytes, exp_bytes)

    def test_write_int(self):
        """Test the write command."""
        self.runner.invoke(spi.write, ["43981"])
        exp_bytes = [0, 0, 171, 205]
        self.assertListEqual(spi.spi_ctrl.SPI_IF.spi_if.tx_bytes, exp_bytes)

    def test_write_with_crc(self):
        """Test the write command with CRC."""
        self.runner.invoke(spi.write, ["0xDEADBEEF", "--crc"])
        exp_bytes = [222, 173, 190, 239, 210]
        self.assertListEqual(spi.spi_ctrl.SPI_IF.spi_if.tx_bytes, exp_bytes)

    def test_read(self):
        """Test the read command."""
        spi.spi_ctrl.SPI_IF.spi_if.return_value = int("0x5555", 16)
        result = self.runner.invoke(spi.read, ["0xAAAA0000"])
        self.assertEqual(result.output.rstrip(), "0xaaaa5555")

    def test_read_int(self):
        """Test the read command with integer input."""
        spi.spi_ctrl.SPI_IF.spi_if.return_value = int("0x5555", 16)
        result = self.runner.invoke(spi.read, ["2863267840"])
        self.assertEqual(result.output.rstrip(), "0xaaaa5555")

    def test_read_with_crc(self):
        """Test the read command."""
        spi.spi_ctrl.SPI_IF.spi_if.return_value = int("0x555544", 16)
        result = self.runner.invoke(spi.read, ["0xAAAA0000", "--crc"])
        self.assertEqual(result.output.rstrip(), "0xaaaa555544")

    def test_gen_crc(self):
        """Test the gen_crc command."""
        result = self.runner.invoke(spi.gen_crc, ["0xF7E6D5C4"])
        self.assertEqual(result.output.rstrip(), "0x4e")
