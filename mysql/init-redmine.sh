#! /bin/sh

while :
do
	mysql -u root -e exit >/dev/null 2>&1 && break
	sleep 5
done

set -e

mysqladmin -u root create redmine

mysql -u root redmine < /redmine.sql
