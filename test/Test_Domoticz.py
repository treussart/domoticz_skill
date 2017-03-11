import unittest
import ConfigParser
import os
from Domoticz import Domoticz

class TestDomoticz(unittest.TestCase):

    def test_init(self):
        config_name = "conf.cfg"
        config_file = os.path.join(os.path.dirname(__file__), config_name)
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        host = self.config.get('domoticz', 'host')
        port = self.config.get('domoticz', 'port')
        self.assertIsInstance(host, str)
        self.assertEqual("192.168.0.1", host)
        self.assertIsInstance(int(port),int)
        self.assertEqual("8080", port)

    def test_convert_name_to_idx(self):
        domoticz = Domoticz()
        idx = domoticz.convert_name_to_idx("Test-Test room")
        self.assertEqual(9999, idx)
        idx = domoticz.convert_name_to_idx("test-test room")
        self.assertEqual(9999, idx)
        idx = domoticz.convert_name_to_idx(" test-Test room ")
        self.assertEqual(9999, idx)
        idx = domoticz.convert_name_to_idx(" test-Te45ilpst room ")
        self.assertEqual(0, idx)
        idx = domoticz.convert_name_to_idx("test-test")
        self.assertEqual(9998, idx)
        idx = domoticz.convert_name_to_idx("Test-test")
        self.assertEqual(9998, idx)
        idx = domoticz.convert_name_to_idx("test-test2")
        self.assertEqual(9997, idx)
        idx = domoticz.convert_name_to_idx("test- test2")
        self.assertEqual(9997, idx)

    def test_switch(self):
        pass

    def test_get(self):
        pass
