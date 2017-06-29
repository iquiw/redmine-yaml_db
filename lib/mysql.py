class MySQL:
    __name = 'redmine-yaml_db-mysql'
    __envs = [ 'MYSQL_ALLOW_EMPTY_PASSWORD=yes',
               'MYSQL_DATABASE=redmine',
               'MYSQL_USER=redmine',
               'MYSQL_PASSWORD=redmine' ]

    def __init__(self, client):
        self.client = client
        self.__build()

    def __build(self):
        self.client.images.build(path = 'mysql', rm = True, tag = MySQL.__name)

    def load_db(self):
        self.container = self.client.containers.run(MySQL.__name,
                                                    detach = True,
                                                    environment = MySQL.__envs)

        ready = 0
        for line in self.container.logs(stdout = False,
                                        stderr = True,
                                        stream = True):
            if b'redmine.sql' in line or b'ready for connections' in line:
                ready += 1
            if ready >= 2:
                break

    def release(self):
        self.container.stop()
        self.container.remove()
