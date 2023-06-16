"""Module for all RPi GPIO related functionality."""
try:
    # pylint: disable-next=consider-using-from-import
    import RPi.GPIO as GPIO

    RPI_VALID = True
except ModuleNotFoundError:
    RPI_VALID = False


def gpio_config():
    """Configure known GPIO pins."""
    if not RPI_VALID:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def set_gpio_dir(channel, direction="input"):
    """Set any GPIO channel as input or output."""
    if not RPI_VALID:
        return
    gpio_config()
    if direction == "output":
        GPIO.setup(channel, GPIO.OUT)
        return
    GPIO.setup(channel, GPIO.IN)


def read_gpio(channel):
    """Read value on any GPIO pin."""
    if not RPI_VALID:
        return 0
    gpio_config()
    set_gpio_dir(channel, "input")
    return GPIO.input(channel)


def toggle_gpio(channel: int):
    """Toggle a GPIO."""
    GPIO.output(channel, not GPIO.input(channel))


def set_gpio(channel: int, state: int, skip_config=False):
    """Set any GPIO channel to a given state."""
    if not RPI_VALID:
        return
    gpio_config()
    set_gpio_dir(channel, "output")
    GPIO.output(channel, state)


def cleanup():
    """Clean all GPIO states."""
    if not RPI_VALID:
        return
    GPIO.cleanup()


def pwm(channel, frequency, dutycycle=50):
    """Set a GPIO channel to use PWM."""
    set_gpio(channel, 0)
    pwm_ch = GPIO.PWM(channel, frequency)
    pwm_ch.start(dutycycle)
    return pwm_ch
