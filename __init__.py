# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from os.path import dirname, abspath
import sys
import re
__author__ = 'mTreussart'

sys.path.append(abspath(dirname(__file__)))
Domoticz = __import__('Domoticz').Domoticz
LOGGER = getLogger(__name__)


class DomoticzSkill(MycroftSkill):

    def __init__(self):
        super(DomoticzSkill, self).__init__(name="DomoticzSkill")

    def initialize(self):
        domoticz_switch_intent = IntentBuilder("SwitchIntent")\
            .optionally("TurnKeyword")\
            .require("StateKeyword")\
            .require("WhatKeyword")\
            .require("WhereKeyword").build()
        self.register_intent(domoticz_switch_intent,
                             self.handle_domoticz_switch_intent)

        domoticz_infos_intent = IntentBuilder("InfosIntent")\
            .require("InfosKeyword")\
            .require("WhatKeyword")\
            .optionally("WhereKeyword")\
            .optionally("StateKeyword").build()
        self.register_intent(domoticz_infos_intent,
                             self.handle_domoticz_infos_intent)

    def handle_domoticz_switch_intent(self, message):
        domoticz = Domoticz()
        state = message.data.get("StateKeyword")
        what = message.data.get("WhatKeyword")
        where = message.data.get("WhereKeyword")
        data = {
            'what': what,
            'where': where
        }
        LOGGER.debug("message : " + str(message.data))
        idx = domoticz.convert_name_to_idx(what, where)
        if idx is 0:
            response = domoticz.switch(state, what, where)
            edng = re.compile(str(state).title(),re.I)
            ending = "ed"
            if edng.search('on') or edng.search('off'):
                ending = ""
            if response is None:
                self.speak_dialog("NotFound", data)
            elif response is 0:
                self.speak("The " + str(what) + " is already " + str(state).title() + ending)
            elif response is 1:
                self.speak("The " + str(what) + " can not be operated with " + str(state).title())
        else:
            LOGGER.debug("idx : " + str(idx))
            domoticz.switchid(state, idx)

    def handle_domoticz_infos_intent(self, message):
        what = message.data.get("WhatKeyword")
        where = message.data.get("WhereKeyword")
        domoticz = Domoticz()
        idx = domoticz.convert_name_to_idx(what, where)
        #idx = 1
        data = {
            'what': what,
            'where': where
        }
        if idx is 0:
            response = domoticz.get(what, where)
            data = str(response['Data'])
            if data is None:
                if where is None:
                    self.speak_dialog("NotFoundShort", data)
                else:
                    self.speak_dialog("NotFound", data)
            if re.search('\d\s+C', data):
                data = data.replace(' C', ' degrees celsius')
            if re.search('\d\s+F', data):
                data = data.replace(' F', ' degrees fahrenheit')
            LOGGER.debug("result : " + str(data))
            self.speak(str(data))
        else:
            response = domoticz.getid(idx)
            data = response['result'][0]['Data']
            if data is None:
                if where is None:
                    self.speak_dialog("NotFoundShort", data)
                else:
                    self.speak_dialog("NotFound", data)
            if re.search('\d\s+C', data):
                data = data.replace(' C', ' degrees celsius')
            if re.search('\d\s+F', data):
                data = data.replace(' F', ' degrees fahrenheit')
            LOGGER.debug("result : " + str(data))
            self.speak(str(data))

    def stop(self):
        pass


def create_skill():
    return DomoticzSkill()
