domoticz_skill
==============

|Licence| |Code Health| |Coverage Status|

+------------------+--------------------+
| Status           | Operating system   |
+==================+====================+
| |Build Status|   | Linux x86\_64      |
+------------------+--------------------+

This skill is for controlling Domoticz with the source voice assistant Mycroft.


Requirements
------------

-  `Python3`_.
-  `Domoticz`_.
-  `Mycroft`_.


Configuration
-------------

Put your configuration in the file “conf.cfg”.

::

    Located in : domoticz_skill/conf.cfg


The principle is to put the 'what' followed by the 'where' separated by a hyphen :

::

   'what-where' = idx


idx is the device number in Domoticz.

examples :

-  temperature-living room = 1
-  flood sensor-bathroom = 2
-  all lights-house = 3
-  Light-Living room = 4

Usage
-----

examples:

In English :

-  turn off the light in the living room
-  turn on the light in the living room
-  can I get temperature in the living room
-  what's the temperature in the living room

In French (not yet tested) :

-  allume la lumière du salon
-  éteind la lumiere du salon


Todo
----

Use with Tasker on Android for send command voice to Mycroft.

.. _Python3: https://www.python.org/downloads/
.. _Mycroft: https://mycroft.ai/
.. _Domoticz: https://domoticz.com/


.. |Licence| image:: https://img.shields.io/packagist/l/doctrine/orm.svg
.. |Code Health| image:: https://landscape.io/github/matleses/domoticz_skill/master/landscape.svg?style=flat
   :target: https://landscape.io/github/matleses/domoticz_skill/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/matleses/domoticz_skill/badge.svg?branch=master
   :target: https://coveralls.io/github/matleses/domoticz_skill?branch=master
.. |Build Status| image:: https://travis-ci.org/matleses/domoticz_skill.svg?branch=master
   :target: https://travis-ci.org/matleses/domoticz_skill
