#!/bin/bash
ssh -C david@slice mysqldump -u$1 -p$1 $1 | mysql -u$1 -p$1 $1
