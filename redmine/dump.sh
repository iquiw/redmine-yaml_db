#! /bin/sh

set -e

/docker-entrypoint.sh rake db:migrate redmine:plugins:migrate
if [ -d plugins/full_text_search ]; then
	/docker-entrypoint.sh rake redmine:plugins:migrate NAME=full_text_search VERSION=0
fi
/docker-entrypoint.sh rake db:dump

cp db/data.yml /data/
