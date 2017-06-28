import docker
from io import BytesIO
import os
import tarfile

from lib.mysql import MySQL
from lib.redmine import Redmine

def docker_copyto(container, srcfile, dstdir):
    tarstream = BytesIO()
    tar = tarfile.open(fileobj = tarstream, mode = 'w')
    tar.add(srcfile)
    tar.close()
    tarstream.seek(os.SEEK_SET)

    return container.put_archive(data = tarstream, path = dstdir)

client = docker.from_env()

volume = client.volumes.create('redmine-yaml_db-data')

mysql = MySQL(client)
mysql.load()
print('Created MySQL container: {0}'.format(mysql.container.short_id))

redmine = Redmine(client)
redmine.dump(mysql, volume)
print('DB dumped to volume: {0}'.format(volume.name))

mysql.release()
