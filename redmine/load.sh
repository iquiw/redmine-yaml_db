#! /bin/sh

set -e

cp /data/data.yml db/

/docker-entrypoint.sh rake db:migrate redmine:plugins:migrate
/docker-entrypoint.sh rake db:load
if [ -d plugins/full_text_search ]; then
	/docker-entrypoint.sh rake redmine:plugins:migrate NAME=full_text_search VERSION=0
fi
/docker-entrypoint.sh rake redmine:plugins:migrate
