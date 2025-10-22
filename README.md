# duy_mock_project

## Create database:
- Log in to MySQL with root user: `sudo mysql -u root -p`
- Create the database: `CREATE DATABASE database_name CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## When installing a new package, please update the requirements.txt file using the following command line below:
- Run: `pip freeze > requirements.txt`

## Install all packages from requirements.txt:
- Run: `pip install -r requirements.txt`

## Add environment variable:
- Create file env: `cp .env.example .env`
- Add value to environment variable in file `.env`
- Please add environment variable to the file `.env.example` if you define a new environment variable

# Database migrations:
- Make migration files: `python manage.py makemigrations your_app`
- Run migration files: `python manage.py migrate your_app`

## Run auto check and fix:
- Run: `black .`

## Run server in local:
- Run `python manage.py runserver`

## Whenever you define a new message, please add it to the locale/vi/LC_MESSAGES/django.po file and run the script to update the locale/vi/LC_MESSAGES/django.mo file.
- Run `python manage.py compilemessages`