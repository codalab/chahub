#!/bin/sh

# Make elasticsearch indexes
# python manage.py search_index --create

echo "Y" | python manage.py search_index --rebuild

# Make a superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python manage.py shell

# Make one extensive fake competition
# python manage.py create_complete_comp --owner admin@admin.com --num-phases 3 --num-participants 128 --num-admins 7 --random-participants 1 --random-admins 1 --title "Factory Generated Competition"

# Make a couple of simple fake competitions
# python manage.py create_comp --number 13 --user admin@admin.com --random 1

python manage.py create_competition --amount 3 --fill-all-details True --fail-on-exception True

# Rebuild elasticsearch indexes if we need to
echo "Y" | python manage.py search_index --rebuild
