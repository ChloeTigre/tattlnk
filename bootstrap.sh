#!/bin/sh
echo -n "Deploying venv if necessary... "
test ! -d venv/ && python3.7 -m venv venv
echo "done"
echo -n "Loading venv... "
. venv/bin/activate
echo "done"
echo -n "Installing dependencies... "
pip3.7 install -r requirements.txt
echo "done"
