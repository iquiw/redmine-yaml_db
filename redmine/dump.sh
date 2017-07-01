#! /bin/sh

set -e

/docker-entrypoint.sh rake db:migrate redmine:plugins:migrate
/docker-entrypoint.sh rake db:dump

cp db/data.yml /data/
