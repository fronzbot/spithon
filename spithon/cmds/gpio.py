"""Raspberry Pi Commands."""
import time
import click
from spithon.core import gpio as gpio_ctrl
from spithon.cmds.common import CONTEXT_SETTINGS


@click.group()
def gpio():
    """GPIO command group."""
    pass


@gpio.command(context_settings=CONTEXT_SETTINGS)
def init():
    """Initialize the GPIO interface."""
    gpio_ctrl.gpio_config()
    click.secho("Done.", fg="green")


@gpio.command(context_settings=CONTEXT_SETTINGS)
def cleanup():
    """Clean up the GPIO interface."""
    gpio_ctrl.cleanup()
    click.secho("Done.", fg="green")


@gpio.command(context_settings=CONTEXT_SETTINGS)
@click.argument("channel", required=True, type=int)
@click.option("--input", "-i", "_input", is_flag=True, help="GPIO as input.")
@click.option("--output", "-o", "_output", is_flag=True, help="GPIO as output.")
def set_dir(channel, _input, _output):
    """Set a GPIO channel to input.

    CHANNEL is the BCM GPIO Channel on the Raspberry Pi.
    """
    direction = None
    if _input and _output:
        click.secho("ERROR: Can only be either input or output, not both.", fg="red")
        return
    if _input:
        direction = "input"
    elif _output:
        direction = "output"
    if direction is None:
        click.secho(
            "ERROR: No direction provided (must be either input or output).", fg="red"
        )
    gpio_ctrl.set_gpio_dir(channel, direction=direction)


@gpio.command(context_settings=CONTEXT_SETTINGS)
@click.argument("channel", required=True, type=int)
def read(channel):
    """Read GPIO state.

    CHANNEL is the BCM GPIO Channel on the Raspberry Pi.
    """
    click.echo(gpio_ctrl.read_gpio(channel))


@gpio.command(context_settings=CONTEXT_SETTINGS)
@click.argument("channel", required=True, type=int)
def drive_lo(channel):
    """Set a GPIO state to 0.

    CHANNEL is the BCM GPIO Channel on the Raspberry Pi
    """
    gpio_ctrl.set_gpio(channel, 0)


@gpio.command(context_settings=CONTEXT_SETTINGS)
@click.argument("channel", required=True, type=int)
def drive_hi(channel):
    """Set a GPIO state to 1.

    CHANNEL is the BCM GPIO Channel on the Raspberry Pi
    """
    gpio_ctrl.set_gpio(channel, 1)


@gpio.command(context_settings=CONTEXT_SETTINGS)
@click.argument("channel", required=True, type=int)
@click.argument("frequency", required=True, type=int)
@click.option("--duty-cycle", "-d", default=50, help="Desired duty cycle.")
def set_pwm(channel, frequency, duty_cycle):
    """Set a GPIO to output PWM.

    CHANNEL is the BCM GPIO Channel on the Raspberry Pi
    FREQUENCY is the desired clock frequency in Hz.
    """
    pwm = gpio_ctrl.pwm(channel, frequency, dutycycle=duty_cycle)
    click.secho("HIT CTRL+C TO EXIT PWM MODE.", fg="magenta")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pwm.stop()


@gpio.command(context_settings=CONTEXT_SETTINGS)
@click.argument("channel", required=True, type=int)
@click.argument("period_ms", required=True, type=float)
@click.option("--once", default=False, is_flag=True, help="Only toggle once.")
def toggle(channel, period_ms, once):
    """Set a GPIO to toggle.

    CHANNEL is the BCM GPIO Channel on the Raspberry Pi
    PERIOD_US is the desired clock period in ms.
    """
    state = 0
    gpio_ctrl.set_gpio(channel, state)
    click.secho("HIT CTRL+C TO EXIT CLOCK MODE.", fg="magenta")
    pulse_width = (period_ms / 2) * 0.001
    if pulse_width < 0.0003:
        click.secho("WARNING: INCOSISTENT FREQUENCIES WITH PERIOD SUB-0.6ms", fg="red")
    try:
        if once:
            gpio_ctrl.toggle_gpio(channel)
            time.sleep(pulse_width)
            gpio_ctrl.toggle_gpio(channel)
            return
        while True:
            gpio_ctrl.toggle_gpio(channel)
            time.sleep(pulse_width)
    except KeyboardInterrupt:
        gpio_ctrl.set_gpio(channel, 0)
