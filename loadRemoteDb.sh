#!/bin/bash
ssh -C david@linode mysqldump -u$1 -p$1 $1 > db.sql
mysql -u$1 -p$1 $1 < db.sql
rm db.sql
