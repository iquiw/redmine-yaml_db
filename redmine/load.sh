#! /bin/sh

set -e

cp /data/data.yml db/

/docker-entrypoint.sh rake db:migrate redmine:plugins:migrate
/docker-entrypoint.sh rake db:load
