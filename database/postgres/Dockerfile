# docker build -t my-postgres-img .

FROM postgres
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB 
#ENV POSTGRES_HOST_AUTH_METHOD scram-sha-256
COPY init/init.sql /docker-entrypoint-initdb.d/