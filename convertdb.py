import docker
import os
import sys
from dotenv import load_dotenv, find_dotenv

from lib.mysql import MySQL
from lib.postgres import Postgres
from lib.redmine import Redmine

if len(sys.argv) < 3:
    print('Usage: {0} INPUT_SQL_FILE OUTPUT_SQL_FILE'.format(sys.argv[0]))
    exit(1)

in_sqlfile  = sys.argv[1]
out_sqlfile = sys.argv[2]

load_dotenv(find_dotenv())
PLUGIN_IMAGE_NAME = os.environ.get('REDMINE_PLUGINS_IMAGE')
client = docker.from_env()

volume = client.volumes.create('redmine-yaml_db-data')
plugins = None
if PLUGIN_IMAGE_NAME is not None:
    plugins = client.containers.run(PLUGIN_IMAGE_NAME, detach = True)

mysql = MySQL(client)
mysql.load_db(in_sqlfile)
print('Created MySQL container: {0}'.format(mysql.container.short_id))

redmine = Redmine(client)
redmine.dump_yaml(mysql, volume, plugins)
print('MySQL DB dumped to volume: {0}'.format(volume.name))

mysql.release()

postgres = Postgres(client)
postgres.run()
print('Created PostgreSQL container: {0}'.format(postgres.container.short_id))

redmine.load_yaml(postgres, volume, plugins)
print('PostgreSQL DB loaded from volume: {0}'.format(volume.name))

postgres.dump_db(out_sqlfile)
print('Dumped to SQL file: {0}'.format(out_sqlfile))

postgres.release()
