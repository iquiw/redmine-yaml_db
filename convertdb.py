import docker

from lib.mysql import MySQL
from lib.redmine import Redmine

client = docker.from_env()

volume = client.volumes.create('redmine-yaml_db-data')

mysql = MySQL(client)
mysql.load()
print('Created MySQL container: {0}'.format(mysql.container.short_id))

redmine = Redmine(client)
redmine.dump(mysql, volume)
print('DB dumped to volume: {0}'.format(volume.name))

mysql.release()
