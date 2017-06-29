#! /bin/sh

set -e

cp /data/data.yml /data/schema.rb db/

/docker-entrypoint.sh rake db:load
