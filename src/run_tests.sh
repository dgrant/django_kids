#!/bin/sh
set -e
coverage run --branch manage.py test --settings=django_kids.settings.test
coverage report
