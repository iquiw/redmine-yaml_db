import docker
from io import BytesIO
import os
import tarfile

def docker_copyto(container, srcfile, dstdir):
    tarstream = BytesIO()
    tar = tarfile.open(fileobj = tarstream, mode = 'w')
    tar.add(srcfile)
    tar.close()
    tarstream.seek(os.SEEK_SET)

    return container.put_archive(data = tarstream, path = dstdir)

def run_mysql(client):
    client.images.build(path = 'mysql', tag = 'redmine-yaml_db-mysql')

    container = client.containers.run('redmine-yaml_db-mysql',
                                      detach = True,
                                      environment = ['MYSQL_ALLOW_EMPTY_PASSWORD=yes',
                                                     'MYSQL_DATABASE=redmine',
                                                     'MYSQL_USER=redmine',
                                                     'MYSQL_PASSWORD=redmine'])

    ready = 0
    for line in container.logs(stdout = False, stderr = True, stream = True):
        if 'redmine.sql' in line or 'ready for connections' in line:
            ready += 1
        if ready >= 2:
            break

    return container

def run_redmine(client, mysql):
    client.images.build(path = 'redmine', tag = 'redmine-yaml_db-redmine')

    container = client.containers.run('redmine-yaml_db-redmine',
                                      command  = '-c "/docker-entrypoint.sh rake db:dump; sleep 600"',
                                      environment = ['REDMINE_DB_MYSQL=' + mysql.name,
                                                     'REDMINE_DB_USERNAME=redmine',
                                                     'REDMINE_DB_PASSWORD=redmine'],
                                      entrypoint = '/bin/sh',
                                      links = [(mysql.name, 'db')])
    return container

client = docker.from_env()
mysql = run_mysql(client)
print(mysql)
redmine = run_redmine(client, mysql)
print(redmine)
mysql.stop()
mysql.remove()
