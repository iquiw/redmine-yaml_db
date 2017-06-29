FROM redmine

RUN sed --in-place '/gosu redmine rake db:migrate/a gosu redmine rake redmine:plugins:migrate' /docker-entrypoint.sh
RUN echo 'gem "yaml_db"' >> Gemfile

COPY dump.sh load.sh /
