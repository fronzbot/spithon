"""SPI configuration creation and loading."""
import os
import configparser
from cachetools import TTLCache, cached

try:
    import spidev

    SPI_VALID = True
except ModuleNotFoundError:
    SPI_VALID = False

HOME_DIR = os.path.expanduser("~")
SAVE_DIR = os.path.join(HOME_DIR, ".spithon")
CFG_FILE = os.path.join(SAVE_DIR, "config.ini")
CACHE = TTLCache(maxsize=100, ttl=86400)

# SPI CONFIG DEFAULTS
SPI_BUS = 0

# This is the CE pin of the Raspberry Pi
SPI_DEVICE = 0

SPI_MODE = 0b00
SPI_RATE = 4000000
SPI_BITS_PER_TX = 8

# How many bits for a given word
SPI_WORD_LENGTH = 32


# CRC CONFIG DEFAULTS
CRC_WIDTH = 8
CRC_POLY = "0x10"
CRC_INITIAL_VALUE = 0


class SpiInterface:
    """Class to retain SPI configuration information."""

    def __init__(self, device="RPi.SPI"):
        """Initialize a SPI Interface class."""
        self.data = load_cfg(device=device)
        self.spi_if = None
        self.bus = int(self.data["bus"])
        self.device = int(self.data["device"])
        self.mode = int(self.data["mode"])
        self.sclk_hz = int(self.data["rate"])
        self.bits_per_word = int(self.data["bits_per_tx"])
        self.word_length = int(self.data["word_length"])
        self.num_bytes = int(self.word_length / 8)
        if SPI_VALID:
            self.configure()

    def configure(self):
        """Configure a SPI class."""
        self.spi_if = spidev.SpiDev()
        self.spi_if.open(self.bus, self.device)
        self.spi_if.mode = self.mode
        self.spi_if.max_speed_hz = self.sclk_hz
        self.spi_if.bits_per_word = self.bits_per_word

    def close(self):
        """Close a SPI Interface."""
        self.spi_if.close()


class CRCHandler:
    """Class to handle CRC stuff."""

    def __init__(self, device="RPi.CRC"):
        """Initialize a CRC class."""
        self.data = load_cfg(device=device)
        self.poly = int(self.data["polynomial"], 16)
        self.width = int(self.data["width"])
        self.initial = int(self.data["initial_value"])
        self.num_bytes = int(self.width / 8)


def make_cfg():
    """Generate a config file."""
    if not os.path.exists(SAVE_DIR):
        os.mkdir(SAVE_DIR)

    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section("RPi.SPI")
    config.set("RPi.SPI", "bus", str(SPI_BUS))
    config.set("RPi.SPI", "device", str(SPI_DEVICE))
    config.set("RPi.SPI", "mode", str(SPI_MODE))
    config.set("RPi.SPI", "rate", str(SPI_RATE))
    config.set("RPi.SPI", "bits_per_tx", str(SPI_BITS_PER_TX))
    config.set("RPi.SPI", "word_length", str(SPI_WORD_LENGTH))

    config.add_section("RPi.CRC")
    config.set("RPi.CRC", "width", str(CRC_WIDTH))
    config.set("RPi.CRC", "polynomial", str(CRC_POLY))
    config.set("RPi.CRC", "initial_value", str(CRC_INITIAL_VALUE))

    with open(CFG_FILE, "w", encoding="UTF-8") as out_file:
        config.write(out_file)


@cached(CACHE)
def load_cfg(device="RPi.SPI"):
    """Load a configuration file and return data."""
    if not os.path.isfile(CFG_FILE):
        make_cfg()

    config = configparser.ConfigParser()
    config.read(CFG_FILE)

    return config[device]
