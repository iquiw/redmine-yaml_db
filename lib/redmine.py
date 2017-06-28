class Redmine:
    __name = 'redmine-yaml_db-redmine'

    def __init__(self, client):
        self.client = client
        self.__build()

    def __build(self):
        self.client.images.build(path = 'redmine', rm = True, tag = Redmine.__name)

    def __run(self, command, environment, dbname, volume):
        self.client.containers.run(
            Redmine.__name,
            command = command,
            environment = environment,
            entrypoint = '/bin/sh',
            links = [(dbname, 'db')],
            remove = True,
            volumes = { volume.name: { 'bind': '/data', 'mode': 'rw' }})

    def dump(self, mysql, volume):
        self.__run('/dump.sh',
                   [ 'REDMINE_DB_MYSQL=' + mysql.container.name,
                     'REDMINE_DB_USERNAME=redmine',
                     'REDMINE_DB_PASSWORD=redmine' ],
                   mysql.container.name,
                   volume)
