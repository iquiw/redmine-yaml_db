import docker
from pathlib import Path

from lib.mysql import MySQL
from lib.postgres import Postgres
from lib.redmine import Redmine

sql_file = Path('mysql/redmine.sql')
if not sql_file.exists():
    print('Please put SQL file: {0}'.format(str(sql_file)))
    exit(1)

client = docker.from_env()

volume = client.volumes.create('redmine-yaml_db-data')

mysql = MySQL(client)
mysql.load_db()
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
