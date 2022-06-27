FROM snakepacker/python:all as builder

RUN python3.10 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt

COPY dist/ /mnt/dist/
RUN /usr/share/python3/app/bin/pip install /mnt/dist/* \
    && /usr/share/python3/app/bin/pip check

FROM snakepacker/python:3.10 as api

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/analyzer-* /usr/local/bin/

ENV analyzer_port 8080

CMD ["analyzer-api"]

FROM ubuntu:20.04

RUN apt-get update && apt-get install -y wget gnupg2 lsb-release

RUN  sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -


## Import the repository signing key:
#RUN wget http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc
#
#RUN apt-key add ACCC4CF8.asc

#RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

RUN apt-get update

RUN bash -c 'apt list postgresql'

ARG TZ=Etc/UTC
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y install postgresql-14

USER postgres

RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER posgres WITH SUPERUSER PASSWORD 'admin';" &&\
    createdb -O posgres market

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/14/main/pg_hba.conf

RUN echo "listen_addresses='*'" >> /etc/postgresql/14/main/postgresql.conf

EXPOSE 5432

VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["/usr/lib/postgresql/14/bin/postgres", "-D", "/var/lib/postgresql/14/main", "-c", "config_file=/etc/postgresql/14/main/postgresql.conf"]