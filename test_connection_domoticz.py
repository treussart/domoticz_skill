"""For testing Domoticz connection."""
import urllib


host = "127.0.0.1"
port = "80"
protocol = False
authentication = False
if protocol:
    protocol = "https"
else:
    protocol = "http"
if authentication:
    login = "user"
    password = "password"
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
