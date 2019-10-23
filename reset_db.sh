#!/usr/bin/env bash

docker-compose exec postgres bash -c "
echo 'dropping database'
dropdb --if-exists -U \$DB_USER \$DB_NAME &&
echo \$DB_PASSWORD &&
echo 'drop successful'
echo 'creating db'
createdb -U \$DB_USER \$DB_NAME &&
echo 'create successful'
exit" &&

docker-compose exec django bash -c "
python manage.py migrate &&
python manage.py generate_data -s 3
python manage.py search_index --rebuild -f
exit"
