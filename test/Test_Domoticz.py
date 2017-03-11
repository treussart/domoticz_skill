import unittest
from Domoticz import Domoticz


class TestDomoticz(unittest.TestCase):

    def test_init(self):
        domoticz = Domoticz()
        domoticz.__init__()
        self.assertIsInstance(domoticz.host, str)
        self.assertIsInstance(int(domoticz.port), int)

    def test_convert_name_to_idx(self):
        domoticz = Domoticz()
        idx = domoticz.convert_name_to_idx("Test", "test room")
        self.assertEqual('9999', idx)
        idx = domoticz.convert_name_to_idx("test", "test room")
        self.assertEqual('9999', idx)
        idx = domoticz.convert_name_to_idx(" test", "Test room ")
        self.assertEqual('9999', idx)
        idx = domoticz.convert_name_to_idx(" test", "Te45ilpst room ")
        self.assertEqual(0, idx)
        idx = domoticz.convert_name_to_idx(" test2", None)
        self.assertEqual(0, idx)
        idx = domoticz.convert_name_to_idx("test", None)
        self.assertEqual('9998', idx)

    def test_switch(self):
        domoticz = Domoticz()
        response = domoticz.switch("on", 12)
        self.assertEqual('{\n   "status" : "ERR"\n}\n', response)
        response = domoticz.switch("On", 12)
        self.assertEqual('{\n   "status" : "ERR"\n}\n', response)
        response = domoticz.switch(12, "On")
        self.assertEqual('{\n   "status" : "ERR"\n}\n', response)
        response = domoticz.switch("On", "test")
        self.assertEqual('{\n   "status" : "ERR"\n}\n', response)

    def test_get(self):
        domoticz = Domoticz()
        response = domoticz.get(12)
        self.assertIn("u'status': u'OK'", str(response))
        response = domoticz.get("12")
        self.assertIn("u'status': u'OK'", str(response))
        response = domoticz.get("test")
        self.assertIn("u'status': u'OK'", str(response))


if __name__ == '__main__':
    unittest.main()
