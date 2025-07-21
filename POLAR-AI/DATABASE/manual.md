## Docker for RasperriPi 5

Does not work on arm the same way as x64 or x86

### Instalation script
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

## Manually execute SQL scripts

When having problems with the container, we shall execute the scripts manually to create the tables and insert the data

### Access the container
```bash
sudo docker exec -it polar_postgres bash
```

### Access the database
```bash
psql -U node_admin -d node_db
```

### Execute the scripts
```bash
\i /docker-entrypoint-initdb.d/init.sql
\i /docker-entrypoint-initdb.d/content.sql
```