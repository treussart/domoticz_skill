import urllib
import ConfigParser
import os
import json
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)


class Domoticz:

    def __init__(self):
        config_name = "conf.cfg"
        config_file = os.path.join(os.path.dirname(__file__), config_name)
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)
        self.host = self.config.get('domoticz', 'host')
        self.port = self.config.get('domoticz', 'port')
        self.url = "http://" + self.host + ":" + self.port

    def convert_name_to_idx(self, what, where):
        if where is None:
            for (key, val) in self.config.items("devices"):
                if what.lower().strip() == key.lower().strip():
                    return val
        else:
            for (key, val) in self.config.items("devices"):
                if what.lower().strip() + "-" + where.lower().strip() == key.lower().strip():
                    return val
        return 0

    def switch(self, state, idx):
        try:
            f = urllib.urlopen(self.url + "/json.htm?type=command&param=switchlight&idx=" + str(idx) + "&switchcmd=" + str(state).title())
            response = f.read()
            LOGGER.debug(str(response))
            return response
        except IOError as e:
            LOGGER.error(str(e) + ' : ' + str(e.read()))

    def get(self, idx):
        try:
            f = urllib.urlopen(self.url + "/json.htm?type=devices&rid=" + str(idx))
            response = f.read()
            return json.loads(response)
        except IOError as e:
            LOGGER.error(str(e) + ' : ' + str(e.read()))
