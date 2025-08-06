#!/bin/bash
cd /home/oliver/Documents/Software\ Class/pwa_project/pwa_project
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
echo "Migrations completed successfully!" 