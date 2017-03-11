#!/usr/bin/env bash

virtualenv --python=python2.7 .venv
source .venv/bin/activate
pip install mycroft_skills_sdk --extra-index-url=http://pypi.mycroft.team --trusted-host pypi.mycroft.team
pip install -r test-requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)

coverage erase
coverage run test/Test_Domoticz.py
#coverage run -a test/Test_init.py

coverage report -i

#coverage html

flake8 .