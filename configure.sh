#!/bin/bash
sudo apt-get update
sudo apt-get install -y python-setuptools python-dev build-essential
sudo easy_install pip
sudo pip install virtualenv
virtualenv --python=python3 venv
venv/bin/python3 -m pip install -r requirements.txt
