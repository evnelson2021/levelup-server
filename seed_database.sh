#!/bin/bash

rm db.sqlite3
rm -rf ./levelupapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations levelupapi
python3 manage.py migrate levelupapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata gamers
python3 manage.py loaddata game_types
python3 manage.py loaddata games
python3 manage.py loaddata events
python3 manage.py loaddata attendees


# Run this command to seed database:    chmod u+x ./seed_database.sh