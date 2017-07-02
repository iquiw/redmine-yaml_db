import docker
from pathlib import Path
import sys

from lib.mysql import MySQL
from lib.postgres import Postgres
from lib.redmine import Redmine

if len(sys.argv) < 3:
    print('Usage: {0} INPUT_SQL_FILE OUTPUT_SQL_FILE'.format(sys.argv[0]))
    exit(1)

in_sqlfile  = sys.argv[1]
out_sqlfile = sys.argv[2]

client = docker.from_env()

volume = client.volumes.create('redmine-yaml_db-data')

mysql = MySQL(client)
mysql.load_db(in_sqlfile)
print('Created MySQL container: {0}'.format(mysql.container.short_id))

redmine = Redmine(client)
redmine.dump_yaml(mysql, volume)
print('MySQL DB dumped to volume: {0}'.format(volume.name))

mysql.release()

postgres = Postgres(client)
postgres.run()
print('Created PostgreSQL container: {0}'.format(postgres.container.short_id))

redmine.load_yaml(postgres, volume)
print('PostgreSQL DB loaded from volume: {0}'.format(volume.name))

postgres.dump_db(out_sqlfile)
print('Dumped to SQL file: {0}'.format(out_sqlfile))

postgres.release()
