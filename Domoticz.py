"""For controlling Domoticz."""
import urllib
import urllib.request
import json
import re
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)


class Domoticz:
    """Class for controlling Domoticz."""
    def __init__(self, host, port, protocol, authentication, login, password):
        """Recover settings for accessing to Domoticz instance."""
        self.host = host
        self.port = port
        protocol = protocol
        authentication = authentication
        if protocol:
            self.protocol = "https"
        else:
            self.protocol = "http"
        if authentication:
            self.login = login
            self.password = password
            self.url = self.protocol + "://" + self.login + ":" + self.password + "@" + self.host + ":" + self.port
        else:
            self.url = self.protocol + "://" + self.host + ":" + self.port

    def findid(self, what, where, state):
        i = 0
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        f = urllib.request.urlopen(self.url + "/json.htm?type=devices&filter=all&used=true")
        response = f.read()
        payload = json.loads(response.decode('utf-8'))
        idx = False
        stype = False
        dlevel = False
        while i < len(payload['result']):
            if whr.search(payload['result'][i]['Name']) and wht.search(payload['result'][i]['Name']):
                stype = payload['result'][i]['Type']
                typ = re.compile(stype, re.I)
                dlevel = "100"
                if typ.search("Group") or typ.search("Scene"):
                    stype = "scene"
                elif typ.search("Light/Switch"):
                    stype = "light"
                    dlevel = payload['result'][i]['Level']
                else:
                    stype = "light"
                idx = payload['result'][i]['idx']
                rslt = re.compile(" " + str(state).title(), re.I)
                if rslt.search(" " + payload['result'][i]['Data']):
                    result = 0
                else:
                    result = 1
                break
            elif i is len(payload['result']) - 1:
                result = None
                break
            i += 1
        return [idx, result, stype, dlevel]

    def findcmd(self, state, action, dlevel):
        dsrdst = str(state).title()
        act = str(action).title()
        if dsrdst == "None":
            dsrdst = "25%"
        rslt = re.compile(dsrdst, re.I)
        rslt2 = re.compile(act, re.I)
        if dsrdst.find('%') > -1:
            if len(dsrdst) == 3:
                dsrdst = int(dsrdst[0:2])
            elif len(dsrdst) == 4:
                dsrdst = 100
            else:
                dsrdst = 5
        cmd = False
        if rslt2.search('dim') or rslt2.search('decrease'):
            stlvl = int(dlevel) - int(dsrdst)
            if stlvl < 0:
                stlvl = 0
            cmd = "Set%20Level&level=" + str(stlvl)
        elif rslt2.search('brighten') or rslt2.search('increase'):
            stlvl = int(dlevel) + int(dsrdst)
            if stlvl > 100:
                stlvl = 100
            cmd = "Set%20Level&level=" + str(stlvl)
        elif rslt2.search('set'):
            stlvl = int(cmd)
            if stlvl > 100:
                stlvl = 100
            elif stlvl < 0:
                stlvl = 0
            cmd = "Set%20Level&level=" + str(stlvl)
        else:
            if rslt.search('lock') or rslt.search('open') or rslt.search('on'):
                cmd = "On"
            elif rslt.search('unlock') or rslt.search('close') or rslt.search('off'):
                cmd = "Off"
        return cmd

    def switch(self, state, what, where, action):
        """Switch the device in Domoticz."""
        data = []
        data = self.findid(what, where, state)
        idx = data[0]
        result = data[1]
        stype = data[2]
        dlevel = data[3]
        if result is 1:
            cmd = self.findcmd(state, action, dlevel)
            if cmd:
                try:
                    f = urllib.request.urlopen(self.url + "/json.htm?type=command&param=switch" + stype + "&idx=" + str(idx) + "&switchcmd=" + str(cmd))
                    response = f.read()
                    LOGGER.debug(str(response))
                    return response
                except IOError as e:
                    LOGGER.error(str(e) + ' : ' + str(e.read()))
        else:
            LOGGER.debug("no command found")
        return result

    def get(self, what, where):
        """Get the device's data in Domoticz."""
        try:
            f = urllib.request.urlopen(self.url + "/json.htm?type=devices&filter=all&used=true")
            response = f.read()
            payload = json.loads(response.decode('utf-8'))
            wht = re.compile(what, re.I)
            i = 0
            if where is not None:
                whr = re.compile(where, re.I)
                while i < len(payload['result']):
                    if whr.search(payload['result'][i]['Name']) and wht.search(payload['result'][i]['Name']):
                        break
                    elif i is len(payload['result']) - 1:
                        payload['result'][i]['Data'] = None
                        break
                    i += 1
            elif where is None:
                while i < len(payload['result']):
                    if wht.search(payload['result'][i]['Name']):
                        break
                    elif i is len(payload['result']) - 1:
                        payload['result'][i]['Data'] = None
                        break
                    i += 1
            return payload['result'][i]
        except IOError as e:
            LOGGER.error(str(e) + ' : ' + str(e.read()))
