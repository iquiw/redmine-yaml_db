class Postgres:
    __name = 'postgres:9.6'
    __envs = [ 'POSTGRES_DB=redmine',
               'POSTGRES_USER=redmine',
               'POSTGRES_PASSWORD=redmine' ]

    def __init__(self, client):
        self.client = client

    def run(self):
        self.container = self.client.containers.run(Postgres.__name,
                                                    detach = True,
                                                    environment = Postgres.__envs)

    def dump_db(self, sqlfile):
        out = self.container.exec_run('pg_dump -U redmine redmine',
                                      stderr = False,
                                      stream = True)
        with open(sqlfile, 'wb') as f:
            for b in out:
                f.write(b)

    def release(self):
        self.container.stop()
        self.container.remove()
