# This Dockerfile is for the setup of the Database
FROM  postgres:12
COPY rates.sql /docker-entrypoint-initdb.d/
EXPOSE 5432
ENV POSTGRES_PASSWORD=ratestask
