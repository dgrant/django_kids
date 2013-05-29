#!/bin/sh
mkdir static
env/bin/python src/manage.py collectstatic --noinput --link --clear
