#!/usr/bin/env bash
if [[ -z "$DBHOST" || -z "$DBNAME" || -z "$DBUSER" ]]; then
    echo "DBHOST, DBNAME and DBUSER Environment variables must be set".
    exit 1
fi

read -r -d '' query <<- EOF
drop table pokemon_old;
create table pokemon_purge like pokemon;
insert into pokemon_purge select * from pokemon where last_modified > now() - interval 1 hour;
rename table pokemon to pokemon_old;
rename table pokemon_purge to pokemon;
EOF

mysql -h $DBHOST -u $DBUSER -p $DBNAME -e "$query"