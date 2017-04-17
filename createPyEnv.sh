#!/bin/sh
pyenv uninstall -f django-kids-3.6.1
pyenv virtualenv 3.6.1 django-kids-3.6.1
pip install -r requirements.txt
