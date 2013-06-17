#!/bin/sh
cd src
./manage.py test --settings=django_kids.settings.test
cd ..
