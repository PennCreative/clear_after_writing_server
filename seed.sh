#!/bin/bash
rm -rf cawapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations cawapi
python3 manage.py migrate cawapi
python3 manage.py loaddata users
python3 manage.py loaddata journals
python3 manage.py loaddata surveys
python3 manage.py loaddata stats
