#!/bin/sh
cd $(dirname $0)
export PYTHONPATH=..
python3 -m unittest discover -s .
cd -
