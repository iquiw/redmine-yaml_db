class Redmine:
    __name = 'redmine-yaml_db-redmine'

    def __init__(self, client):
        self.client = client
        self.__build()

    def __build(self):
        self.client.images.build(path = 'redmine', rm = True, tag = Redmine.__name)

    def __run(self, command, environment, dbname, volume, plugins):
        self.client.containers.run(
            Redmine.__name,
            command = command,
            environment = environment,
            entrypoint = '/bin/sh',
            links = [(dbname, 'db')],
            remove = True,
            volumes = { volume.name: { 'bind': '/data', 'mode': 'rw' }},
            volumes_from = [ plugins.name ] if plugins is not None else None)

    def dump_yaml(self, mysql, volume, plugins):
        self.__run('/dump.sh',
                   [ 'REDMINE_DB_MYSQL=' + mysql.container.name,
                     'REDMINE_DB_USERNAME=redmine',
                     'REDMINE_DB_PASSWORD=redmine' ],
                   mysql.container.name,
                   volume,
                   plugins)

    def load_yaml(self, postgres, volume, plugins):
        self.__run('/load.sh',
                   [ 'REDMINE_DB_POSTGRES=' + postgres.container.name,
                     'REDMINE_DB_USERNAME=redmine',
                     'REDMINE_DB_PASSWORD=redmine' ],
                   postgres.container.name,
                   volume,
                   plugins)
