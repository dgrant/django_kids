#!/bin/sh
set -e
coverage run manage.py test --settings=django_kids.settings.test
coverage report
