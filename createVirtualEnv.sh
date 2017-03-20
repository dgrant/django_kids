#!/bin/sh
rm -rf env
virtualenv env
env/bin/pip install -r requirements.txt
