"""Test the config.py module."""
from unittest import TestCase, mock
from configparser import ConfigParser
from spithon.core import config


class MockConfigParser(ConfigParser):
    """Mock a config parser class."""

    def __init__(self, **kwargs):
        """Initialize a mock class."""
        super().__init__()
        self.add_section("foobar")
        self.set("foobar", "foo", "bar")

    def read(self, *args, **kwargs):
        """Mock read function."""
        pass


class TestConfig(TestCase):
    """Test class for config."""

    def setUp(self):
        """Set up the config module for testing."""
        config.CACHE.clear()

    @mock.patch("os.path.exists")
    @mock.patch("configparser.ConfigParser.write")
    def test_make_cfg(self, mock_write, mock_exists):
        """Test the make_cfg command."""
        mock_exists.return_value = True
        mock_write.return_value = True
        config.make_cfg()

        mock_exists.assert_called_once_with(config.SAVE_DIR)
        mock_write.assert_called_once()

    @mock.patch("os.path.exists")
    @mock.patch("os.mkdir")
    @mock.patch("configparser.ConfigParser.write")
    def test_make_cfg_no_dir(self, mock_write, mock_dir, mock_exists):
        """Test the make_cfg command with no existing dir."""
        mock_exists.return_value = False
        mock_dir.return_value = True
        mock_write.return_value = True
        config.make_cfg()

        mock_exists.assert_called_once_with(config.SAVE_DIR)
        mock_dir.assert_called_once_with(config.SAVE_DIR)
        mock_write.assert_called_once()

    @mock.patch("os.path.isfile")
    @mock.patch("spithon.core.config.make_cfg")
    @mock.patch("configparser.ConfigParser")
    def test_load_cfg(self, mock_parse, mock_cfg, mock_exists):
        """Test the load_cfg command with existing file."""
        mock_exists.return_value = True
        mock_parse.return_value = MockConfigParser()
        mock_cfg.return_value = True
        result = dict(config.load_cfg(device="foobar"))

        mock_exists.assert_called_once_with(config.CFG_FILE)
        mock_cfg.assert_not_called()
        self.assertEqual(result, {"foo": "bar"})

    @mock.patch("os.path.isfile")
    @mock.patch("spithon.core.config.make_cfg")
    @mock.patch("configparser.ConfigParser")
    def test_load_cfg_cache(self, mock_parse, mock_cfg, mock_exists):
        """Test the load_cfg command caching."""
        mock_exists.return_value = True
        mock_parse.return_value = MockConfigParser()
        mock_cfg.return_value = True
        results = []
        for _ in range(0, 10):
            results.append(dict(config.load_cfg(device="foobar")))

        mock_exists.assert_called_once_with(config.CFG_FILE)
        mock_cfg.assert_not_called()
        for result in results:
            self.assertEqual(result, {"foo": "bar"})

    @mock.patch("os.path.isfile")
    @mock.patch("spithon.core.config.make_cfg")
    @mock.patch("configparser.ConfigParser")
    def test_load_cfg_no_file(self, mock_parse, mock_cfg, mock_exists):
        """Test the load_cfg command without existing faile."""
        mock_exists.return_value = False
        mock_parse.return_value = MockConfigParser()
        mock_cfg.return_value = True
        result = dict(config.load_cfg(device="foobar"))

        mock_exists.assert_called_once_with(config.CFG_FILE)
        mock_cfg.assert_called_once()
        self.assertEqual(result, {"foo": "bar"})

    @mock.patch("os.path.isfile")
    @mock.patch("spithon.core.config.make_cfg")
    @mock.patch("configparser.ConfigParser")
    def test_load_cfg_bad_key(self, mock_parse, mock_cfg, mock_exists):
        """Test the load_cfg command with bad key."""
        mock_exists.return_value = True
        mock_parse.return_value = MockConfigParser()
        mock_cfg.return_value = True
        with self.assertRaises(KeyError):
            config.load_cfg(device="barfoo")

        mock_exists.assert_called_once_with(config.CFG_FILE)
        mock_cfg.assert_not_called()
