"""Test the spi.py module."""
from unittest import TestCase
from unittest.mock import patch
from .. import mock_spidev


with patch("spithon.core.config.load_cfg") as mock_cfg:
    mock_cfg.side_effect = [
        mock_spidev.CFG_MOCK["RPi.SPI"],
        mock_spidev.CFG_MOCK["RPi.CRC"],
    ]
    from spithon.core import spi  # pylint: disable=wrong-import-order


class TestSPI(TestCase):
    """Test class for SPI."""

    def setUp(self):
        """Set up the SPI testing."""
        spi.SPI_VALID = True
        spi.SPI_IF.spi_if = mock_spidev.SpiDev()
        spi.SPI_IF.spi_if.num_bytes = 4
        spi.SPI_IF.num_bytes = 4
        spi.SPI_IF.word_length = 32
        spi.CRC_CFG.width = 8
        spi.CRC_CFG.poly = int("0x37", 16)

    def test_int_to_bytes(self):
        """Test normal functioning of int_to_bytes."""
        value = "0xDEADBEEF"
        exp_value = [222, 173, 190, 239]
        ret_value = spi.int_to_bytes(int(value, 16), length=4, crc=False)
        self.assertListEqual(ret_value, exp_value)

    def test_int_to_bytes_overflow(self):
        """Test if longer word is given the function truncates."""
        value = "0xDEADBEEF"
        with self.assertRaises(OverflowError):
            spi.int_to_bytes(int(value, 16), length=2, crc=False)

    def test_large_word(self):
        """Test with larger word."""
        value = "0xDEADBEEFFEEBDAED"
        spi.SPI_IF.num_bytes = 16
        exp_value = [222, 173, 190, 239, 254, 235, 218, 237]
        ret_value = spi.int_to_bytes(int(value, 16), length=8, crc=False)
        self.assertListEqual(ret_value, exp_value)

    def test_crc8_return(self):
        """Test correct CRC value."""
        value = "0xDEADBEEF"
        spi.CRC_CFG.width = 8
        spi.CRC_CFG.poly = int("0xAB", 16)
        spi.CRC_CFG.initial = 0
        exp_value = int("0x88", 16)
        ret_value = spi.crc_val(value)
        self.assertEqual(ret_value, exp_value)

    def test_crc16_return(self):
        """Test correct CRC value."""
        value = "0xDEADBEEF"
        spi.CRC_CFG.width = 16
        spi.CRC_CFG.poly = int("0xABCD", 16)
        spi.CRC_CFG.initial = 0
        exp_value = int("0xD0EF", 16)
        ret_value = spi.crc_val(value)
        self.assertEqual(ret_value, exp_value)

    def test_crc32_return(self):
        """Test correct CRC value."""
        value = "0xDEADBEEF"
        spi.CRC_CFG.width = 32
        spi.CRC_CFG.poly = int("0xABCD1234", 16)
        spi.CRC_CFG.initial = 0
        exp_value = int("0xF0F92A68", 16)
        ret_value = spi.crc_val(value)
        self.assertEqual(ret_value, exp_value)

    def test_int_to_bytes_with_crc(self):
        """Test int_to_bytes with crc enabled."""
        value = "0xDEADBEEF"
        exp_value = [222, 173, 190, 239, 10]
        ret_value = spi.int_to_bytes(int(value, 16), length=4, crc=True)
        self.assertListEqual(ret_value, exp_value)

    def test_write(self):
        """Test write method."""
        write_val = "0xDEADBEEF"
        exp_bytes = [222, 173, 190, 239]
        spi.spi_write(write_val, crc=False, verbose=False)
        self.assertListEqual(spi.SPI_IF.spi_if.tx_bytes, exp_bytes)

    def test_write_with_int(self):
        """Test write with integer."""
        write_val = int("0xDEADBEEF", 16)
        exp_bytes = [222, 173, 190, 239]
        spi.spi_write(write_val, crc=False, verbose=False)
        self.assertListEqual(spi.SPI_IF.spi_if.tx_bytes, exp_bytes)

    def test_write_with_crc(self):
        """Test write method with CRC enabled."""
        write_val = "0xDEADBEEF"
        exp_bytes = [222, 173, 190, 239, 10]
        spi.spi_write(write_val, crc=True, verbose=False)
        self.assertListEqual(spi.SPI_IF.spi_if.tx_bytes, exp_bytes)

    def test_read(self):
        """Test read method."""
        write_val = "0xDEAD0000"
        spi.SPI_IF.spi_if.return_value = int("0xBEEF", 16)
        exp_word = int("0xDEADBEEF", 16)
        read_word = spi.spi_read(write_val, crc=False, verbose=False)
        self.assertEqual(read_word, exp_word)

    def test_read_with_int(self):
        """Test read method with integer."""
        write_val = int("0xDEAD0000", 16)
        spi.SPI_IF.spi_if.return_value = int("0xBEEF", 16)
        exp_word = int("0xDEADBEEF", 16)
        read_word = spi.spi_read(write_val, crc=False, verbose=False)
        self.assertEqual(read_word, exp_word)

    def test_check_crc8(self):
        """Test check crc8 method with valid data."""
        word = int("0xABCD123", 16)
        spi.CRC_CFG.poly = int("0x5F", 16)
        spi.CRC_CFG.width = 8
        spi.CRC_CFG.initial = int("0xA", 16)
        # This comes from a calculator and is hard-coded
        exp_crc = int("0x70", 16)
        calc_crc = spi.crc_val(word)
        self.assertTrue(spi.check_crc(word, calc_crc), exp_crc)

    def test_check_crc16(self):
        """Test check crc16 method with valid data."""
        word = int("0xABCD123", 16)
        spi.CRC_CFG.poly = int("0x601A", 16)
        spi.CRC_CFG.width = 16
        spi.CRC_CFG.initial = int("0x5", 16)
        # This comes from a calculator and is hard-coded
        exp_crc = int("0xACB2", 16)
        calc_crc = spi.crc_val(word)
        self.assertTrue(spi.check_crc(word, calc_crc), exp_crc)

    def test_check_crc32(self):
        """Test check crc132 method with valid data."""
        word = int("0xABCD123", 16)
        spi.CRC_CFG.poly = int("0xDEADBEEF", 16)
        spi.CRC_CFG.width = 16
        spi.CRC_CFG.initial = int("0x1F", 16)
        # This comes from a calculator and is hard-coded
        exp_crc = int("0x6761C5D9", 16)
        calc_crc = spi.crc_val(word)
        self.assertTrue(spi.check_crc(word, calc_crc), exp_crc)

    def test_check_crc8_fail(self):
        """Test check crc8 method with invalid data."""
        word = int("0xABCD123", 16)
        spi.CRC_CFG.poly = int("0x5F", 16)
        spi.CRC_CFG.width = 8
        spi.CRC_CFG.initial = int("0xA", 16)
        # This comes from a calculator and is hard-coded
        exp_crc = int("0x70", 16)
        calc_crc = spi.crc_val(word) + 1
        self.assertFalse(spi.check_crc(word, calc_crc), exp_crc)

    def test_check_crc16_fail(self):
        """Test check crc16 method with invalid data."""
        word = int("0xABCD123", 16)
        spi.CRC_CFG.poly = int("0x601A", 16)
        spi.CRC_CFG.width = 16
        spi.CRC_CFG.initial = int("0x5", 16)
        # This comes from a calculator and is hard-coded
        exp_crc = int("0xACB2", 16)
        calc_crc = spi.crc_val(word) + 1
        self.assertFalse(spi.check_crc(word, calc_crc), exp_crc)

    def test_check_crc32_fail(self):
        """Test check crc132 method with invalid data."""
        word = int("0xABCD123", 16)
        spi.CRC_CFG.poly = int("0xDEADBEEF", 16)
        spi.CRC_CFG.width = 16
        spi.CRC_CFG.initial = int("0x1F", 16)
        # This comes from a calculator and is hard-coded
        exp_crc = int("0x6761C5D9", 16)
        calc_crc = spi.crc_val(word) + 1
        self.assertFalse(spi.check_crc(word, calc_crc), exp_crc)

    def test_read_with_crc(self):
        """Test read method with CRC."""
        write_val = "0xDEAD0000"
        spi.SPI_IF.spi_if.return_value = int("0xBEEF0A", 16)
        exp_word = int("0xDEADBEEF0A", 16)
        read_word = spi.spi_read(write_val, crc=True, verbose=False)
        self.assertEqual(read_word, exp_word)
