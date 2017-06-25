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

def create_network(client):
    return client.networks.create('redmine-yaml_db', driver = 'bridge')

def run_mysql(client):
    client.images.build(path = 'mysql', tag = 'redmine-yaml_db-mysql')

    container = client.containers.run('redmine-yaml_db-mysql',
                                      detach = True,
                                      environment = ['MYSQL_ALLOW_EMPTY_PASSWORD=yes',
                                                     'MYSQL_USER=redmine',
                                                     'MYSQL_PASSWORD=redmine'],
                                      network = 'redmine-yaml_db')
    print(container)
    container.exec_run('sh /init-redmine.sh')
    return container

def run_redmine(client, mysql):
    client.images.build(path = 'redmine', tag = 'redmine-yaml_db-redmine')

    container = client.containers.run('redmine-yaml_db-redmine',
                                      command  = 'rake db:data:dump; sleep 600',
                                      detach = True,
                                      environment = ['REDMINE_DB_MYSQL=db',
                                                     'REDMINE_DB_USERNAME=redmine',
                                                     'REDMINE_DB_PASSWORD=redmine'],
                                      network = 'redmine-yaml_db',
                                      links = {
                                          container.name: 'db'
                                      })

    return container

client = docker.from_env()
network = create_network(client)
mysql = run_mysql(client)
run_redmine(client, mysql)
