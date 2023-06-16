"""Init file for SPI."""


def conv_to_int(value):
    """Convert an unknown value to an integer."""
    try:
        conv_val = int(value)
    except ValueError:
        # Must be hex
        conv_val = int(value, 16)
    return conv_val
