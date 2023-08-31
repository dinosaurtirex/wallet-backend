# Delete db

```
drop database wallet_db;
```

# Create db 

```
CREATE USER admin_user WITH PASSWORD '69de4794b28b368aec69de4794b2ebef901c1f1968';
CREATE DATABASE wallet_db;
ALTER DATABASE wallet_db SET timezone TO 'Europe/Moscow';

ALTER ROLE admin_user SET client_encoding TO 'utf8';
ALTER ROLE admin_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin_user SET timezone TO 'Europe/Moscow';

GRANT ALL PRIVILEGES ON DATABASE wallet_db TO admin_user;
GRANT ALL ON DATABASE wallet_db TO admin_user;
ALTER DATABASE wallet_db OWNER TO admin_user;
```

# Init orm

```
aerich init -t db.TORTOISE_ORM
aerich init-db
aerich migrate --name init
aerich upgrade
```