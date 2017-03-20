#!/bin/bash
mysqldump -u$1 -p$1 $1 | ssh -C david@linode mysql -u$2 -p$2 $2
