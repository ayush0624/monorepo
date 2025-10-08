# Postgres Instructions

Here are the instructions on how to spin up a postgres server
and apply the database migrations

## Spin Up Basic Server

Load the postgres image into local docker. The current image is for macOS with docker desktop
```bash
bazel run //projects/bookshelf/postgres:load
```

Run the loaded docker image

```bash
docker run -d \
  --name postgres-main \
  -p 5432:5432 \
  postgres:main
```

Connect to the server with psql
```bash
psql -h localhost -p 5432 -U postgres -d appdb
```
The password will be postgres
