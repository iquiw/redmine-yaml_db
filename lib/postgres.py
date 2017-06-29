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

    def release(self):
        self.container.stop()
        self.container.remove()
