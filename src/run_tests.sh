#!/bin/sh
set -e
coverage run --source="/home/david/git/django_kids/src/links" manage.py test --settings=django_kids.settings.test
coverage report --include="/home/david/git/django_kids/src/*" --omit="links/migrations/*,django_kids/settings/*,links/tests/*"
