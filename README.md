# Django Cheatsheet

## Create Project
django-admin startproject mysite

django-admin runserver

## Run Server
```
python manage.py runserver
```

## Create new app in project
* one project can have several apps / one app can be in serveral projects
* a App holds a Data-Model
```
python manage.py startapp polls
python manage.py runserver
```

## migrate initial databases setup (create tabels)
```
python manage.py migrate
```

## migrate initial database setup for new app (create initial tables)
```
python manage.py makemigrations polls
python manage.py migrate
```

## interact with Database-Api
```
python manage.py shell
```

## create admin user
```
python manage.py createsuperuser
```

# Templates

https://docs.djangoproject.com/en/3.0/topics/templates/