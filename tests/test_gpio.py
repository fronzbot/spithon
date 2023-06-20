"""Test the config.py module."""
import sys
from unittest import TestCase
from unittest.mock import patch
import Mock.GPIO

sys.modules["RPi.GPIO"] = Mock.GPIO
# pylint: disable=wrong-import-position
from spithon.core import gpio


class TestConfig(TestCase):
    """Test class for config."""

    def setUp(self):
        """Set up the config module for testing."""
        pass

    @patch("Mock.GPIO.setup")
    def test_set_gpio_dir_input(self, mock_setup):
        """Test the gpio direction setup."""
        gpio.set_gpio_dir(0, "input")
        mock_setup.assert_called_once_with(0, Mock.GPIO.IN)

    @patch("spithon.core.gpio.set_gpio_dir")
    @patch("Mock.GPIO.input")
    def test_read_gpio(self, mock_input, mock_dir):
        """Test the read GPIO functionality."""
        gpio.read_gpio(0)
        mock_dir.assert_called_once_with(0, "input")
        mock_input.assert_called_once_with(0)

    @patch("spithon.core.gpio.set_gpio_dir")
    @patch("Mock.GPIO.output")
    def test_set_gpio(self, mock_output, mock_dir):
        """Test the set GPIO functionality."""
        gpio.set_gpio(0, 0)
        mock_dir.assert_called_once_with(0, "output")
        mock_output.assert_called_once_with(0, 0)

    @patch("Mock.GPIO.input")
    @patch("Mock.GPIO.output")
    def test_toggle_gpio(self, mock_output, mock_input):
        """Test the toggle GPIO functionality."""
        mock_input.return_value = 0
        gpio.toggle_gpio(0)
        mock_output.assert_called_once_with(0, 1)

    @patch("Mock.GPIO.cleanup")
    def test_gpio_cleanup(self, mock_clean):
        """Test the GPIO cleanup functionality."""
        gpio.cleanup()
        mock_clean.assert_called_once()

    def test_gpio_pwm(self):
        """Test the GPIO PWM functionality."""
        pwm = gpio.pwm(0, 1)
        self.assertTrue(isinstance(pwm, Mock.GPIO.PWM))
