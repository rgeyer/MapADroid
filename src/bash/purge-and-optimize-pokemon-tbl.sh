#!/usr/bin/env bash
if [[ -z "$DBHOST" || -z "$DBNAME" || -z "$DBUSER" ]]; then
    echo "DBHOST, DBNAME and DBUSER Environment variables must be set".
    exit 1
fi
mysqldump -h $DBHOST -d -u $DBUSER -p $DBNAME pokemon > pokemon.sql
echo "optimize table pokemon;" >> pokemon.sql
mysql -h $DBHOST -u $DBUSER -p $DBNAME < pokemon.sql
rm -rf pokemon.sql