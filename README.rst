domoticz_skill
==============

|Licence| |Code Health| |Coverage Status| |Documentation Status|

+------------------+--------------------+
| Status           | Operating system   |
+==================+====================+
| |Build Status|   | Linux x86\_64      |
+------------------+--------------------+

Hi!


Requirements
------------

-  `Python2`_.
-  `Domoticz`_.
-  `Mycroft`_.

Documentation
-------------

Read the documentation on `http://domoticz_skill.readthedocs.io/ <http:///domoticz_skill.readthedocs.io/>`_.

Configuration
-------------

Put your configuration in the file “conf.cfg”.

::

    Located in : domoticz_skill/conf.cfg


The principle is to put the 'what' followed by the 'where' separated by a hyphen :

::

   'what-where' = idx

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
-  get temperature in the living room
-  can I get the next trains

In French :
-  allume la lumière du salon
-  éteind la lumiere du salon


Coming Soon
-----------

Use with Tasker on Android for send command voice to Mycroft.

.. _Python2: https://www.python.org/downloads/
.. _Mycroft: https://mycroft.ai/
.. _Domoticz: https://domoticz.com/


.. |Licence| image:: https://img.shields.io/packagist/l/doctrine/orm.svg
.. |Code Health| image:: https://landscape.io/github/matleses/Transilien-Domoticz/master/landscape.svg?style=flat
   :target: https://landscape.io/github/matleses/Transilien-Domoticz/master
.. |Coverage Status| image:: https://coveralls.io/repos/github/matleses/Transilien-Domoticz/badge.svg?branch=master
   :target: https://coveralls.io/github/matleses/Transilien-Domoticz?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/transilien-domoticz/badge/?version=latest
   :target: http://transilien-domoticz.readthedocs.io/?badge=latest
.. |Build Status| image:: https://travis-ci.org/matleses/Transilien-Domoticz.svg?branch=master
   :target: https://travis-ci.org/matleses/Transilien-Domoticz
