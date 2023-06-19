"""Mock the spidev library."""

CFG_MOCK = {
    "RPi.SPI": {
        "bus": 0,
        "device": 0,
        "mode": 0,
        "rate": 1,
        "bits_per_tx": 8,
        "word_length": 32,
    },
    "RPi.CRC": {
        "width": 8,
        "polynomial": "0x10",
        "initial_value": 0,
    },
}


class SpiDev:
    """Class to mock a spidev class."""

    def __init__(self):
        """Initialize a SpiDev class."""
        self.tx_bytes = None
        self._return_value = None
        self.mode = None
        self.max_speed_hz = None
        self.bits_per_word = None
        self.cshigh = None
        self.loop = None
        self.no_cs = None
        self.lsbfirst = None
        self.threewire = None
        self.read0 = None
        self.num_bytes = 8

    @property
    def return_value(self):
        """Return the set return value."""
        return self._return_value

    @return_value.setter
    def return_value(self, value):
        """Convert integer return value to bytes."""
        self._return_value = bytearray(value.to_bytes(self.num_bytes, "big"))

    def open(self, *args, **kwawrgs):
        """Mock an open class."""
        pass

    def close(self, *args, **kwargs):
        """Mock a close class."""
        pass

    def xfer(self, *args, **kwargs):
        """Mock a transfer class."""
        self.tx_bytes = args[0]
        return self.return_value

    def xfer2(self, *args, **kwargs):
        """Mock a xfer2 class."""
        return self.xfer(args, kwargs)

    def xfer3(self, *args, **kwargs):
        """Mock a xfer3 class."""
        return self.xfer(args, kwargs)
