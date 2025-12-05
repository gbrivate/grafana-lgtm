FROM postgres:17-alpine

# Define variáveis (não coloque senhas fixas em produção)
ENV POSTGRES_USER=myuser \
    POSTGRES_PASSWORD=mypassword \
    POSTGRES_DB=mydb

COPY postgresql.conf.sample /usr/local/share/postgresql/postgresql.conf.sample

# Enable structured logging in the default configuration file
#RUN echo "logging_collector = on" >> /usr/local/share/postgresql/postgresql.conf.sample \
 #   && echo "log_destination = 'stderr'" >> /usr/local/share/postgresql/postgresql.conf.sample \
  #  && echo "log_line_prefix = '%m [%p] trace_id=%a user=%u db=%d '" >> /usr/local/share/postgresql/postgresql.conf.sample \
  #  && echo "log_statement = 'all'" >> /usr/local/share/postgresql/postgresql.conf.sample \
  #  && echo "log_min_duration_statement = 300ms" >> /usr/local/share/postgresql/postgresql.conf.sample \
  #  && echo "shared_preload_libraries = 'pg_stat_statements'" >> /usr/local/share/postgresql/postgresql.conf.sample \
  #  && echo "event_source.track = 'PostgreSQL'" >> /usr/local/share/postgresql/postgresql.conf.sample


# Expor a porta
EXPOSE 5432
