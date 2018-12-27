"""For controlling Domoticz."""
import urllib
import urllib.request
import configparser
import os
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

    def switch(self, state, what, where, action):
        """Switch the device in Domoticz."""
        i = 0
        wht = re.compile(what,re.I)
        whr = re.compile(where,re.I)
        f = urllib.request.urlopen(self.url + "/json.htm?type=devices&filter=all&used=true")
        response = f.read()
        payload = json.loads(response.decode('utf-8'))
        idx = []
        while i < len(payload['result']):
            if  whr.search(payload['result'][i]['Name']) and wht.search(payload['result'][i]['Name']):
                stype = payload['result'][i]['Type']
                typ = re.compile(stype,re.I)
                dtype = "None"
                dlevel = "100"
                if typ.search("Group") or typ.search("Scene"):
                    stype = "scene"
                elif typ.search("Light/Switch"):
                    stype = "light"
                    dtype = payload['result'][i]['SwitchType']
                    dlevel = payload['result'][i]['Level']
                else:
                    stype = "light"
                idx = payload['result'][i]['idx']
                dtyp = re.compile(dtype,re.I)
                rslt = re.compile(" " + str(state).title(),re.I)
                if rslt.search(" " + payload['result'][i]['Data']):
                    result = 0
                else:
                    result = 1
                break
            elif i is len(payload['result'])-1:
                result = None
                break
            i += 1
        #i -= 1
        if result is 1:
            cmd = str(state).title()
            act = str(action).title()
            if cmd == "None":
                cmd = "25%"
            rslt = re.compile(cmd,re.I)
            rslt2 = re.compile(act,re.I)
            if cmd.find('%') > -1:
                if len(cmd) == 3:
                    cmd = int(cmd[0:2])
                elif len(cmd) == 4:
                    cmd = 100
                else:
                    cmd = 5
            dropout = 1
            if rslt2.search('dim') or rslt2.search('decrease'):
                stlvl = int(dlevel)-int(cmd)
                if stlvl < 0:
                    stlvl = 0
                cmd = "Set%20Level&level=" + str(stlvl)
                dropout = 0
            elif rslt2.search('brighten') or rslt2.search('increase'):
                stlvl = int(dlevel)+int(cmd)
                if stlvl > 100:
                    stlvl = 100
                cmd = "Set%20Level&level=" + str(stlvl)
                dropout = 0
            elif rslt2.search('set'):
                stlvl = int(cmd)
                if stlvl > 100:
                    stlvl = 100
                elif stlvl < 0:
                    stlvl = 0
                cmd = "Set%20Level&level=" + str(stlvl)
                dropout = 0
            else:
                if rslt.search('lock') or rslt.search('open'):
                    cmd = "On"
                    dropout = 0
                elif rslt.search('unlock') or rslt.search('close'):
                    cmd = "Off"
                    dropout = 0
                elif rslt.search('on') or rslt.search('off'):
                    dropout = 0
            if dropout is 0:
                try:
                    f = urllib.request.urlopen(self.url + "/json.htm?type=command&param=switch" + stype + "&idx=" + str(idx) + "&switchcmd=" + str(cmd))
                    response = f.read()
                    LOGGER.debug(str(response))
                    return response
                except IOError as e:
                    LOGGER.error(str(e) + ' : ' + str(e.read()))
            else:
                LOGGER.debug(str(act) + str(dropout) + str(cmd))
        return result

    def get(self, what, where):
        """Get the device's data in Domoticz."""
        try:
            f = urllib.request.urlopen(self.url + "/json.htm?type=devices&filter=all&used=true")
            response = f.read()
            payload = json.loads(response.decode('utf-8'))
            wht = re.compile(what,re.I)
            i = 0
            if where is not None:
                whr = re.compile(where,re.I)
                while i < len(payload['result']):
                    if  whr.search(payload['result'][i]['Name']) and wht.search(payload['result'][i]['Name']):
                        break
                    elif i is len(payload['result'])-1:
                        payload['result'][i]['Data'] = None
                        break
                    i += 1
            elif where is None:
                while i < len(payload['result']):
                    if  wht.search(payload['result'][i]['Name']):
                        break
                    elif i is len(payload['result'])-1:
                        payload['result'][i]['Data'] = None
                        break
                    i += 1
            return payload['result'][i]
            #return devices.data
            #return json.loads(response.decode('utf-8'))
        except IOError as e:
            LOGGER.error(str(e) + ' : ' + str(e.read()))
