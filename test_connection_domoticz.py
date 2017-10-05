"""For testing Domoticz connection."""
import urllib
import ConfigParser
import os


config_name = "conf.cfg"
config_file = os.path.join(os.path.dirname(__file__), config_name)
config = ConfigParser.ConfigParser()
config.read(config_file)
host = config.get('domoticz', 'host')
port = config.get('domoticz', 'port')
protocol = config.get('domoticz', 'protocol')
if config.get('domoticz', 'authentication') is "True":
    login = config.get('domoticz', 'login')
    password = config.get('domoticz', 'password')
    url = protocol + "://" + login + ":" + password + "@" + host + ":" + port
else:
    url = protocol + "://" + host + ":" + port
try:
    f = urllib.urlopen(url + "/json.htm?type=devices&used=true&filter=all")
    if f.getcode() == 200:
        print("Connection OK")
    else:
        print("Connection KO")

except Exception as e:
    print("Connection KO: " + str(e.__str__()))
