#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

echo "colecting Static..."
python manage.py collectstatic --no-input

echo "Make Migration..."
python manage.py makemigrations --noinput
python manage.py migrate