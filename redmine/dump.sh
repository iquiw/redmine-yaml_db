#! /bin/sh

set -e

/docker-entrypoint.sh rake db:dump

cp db/data.yml db/schema.rb /data/
