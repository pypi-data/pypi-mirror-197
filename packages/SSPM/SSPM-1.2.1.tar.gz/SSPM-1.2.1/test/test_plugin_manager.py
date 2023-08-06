import unittest
from sspm import PluginManager


class TestPluginManager(unittest.TestCase):

    def setUp(self) -> None:
        self.plugin_manager = PluginManager("./test_files/plugins")
        self.plugin_manager.import_plugins()

    def test_plugin_manager(self):
        self.assertIsNotNone(self.plugin_manager)

    def test_plugin_import(self):
        self.assertIsNotNone(self.plugin_manager.active_plugins)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestPluginManager)
])
