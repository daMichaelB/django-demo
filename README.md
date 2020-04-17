# Django Cheatsheet

## Create Project
```
django-admin startproject mysite
```

To complete the project setup, you need to create the tables associated with the models of the applications listed in `settings.py` : `INSTALLED_APPS`.

```
python manage.py migrate
```

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
```bash
python manage.py makemigrations polls  # create migration file
python manage.py sqlmigrate polls 0001  # view all sql commands
python manage.py migrate # apply migration
```

## create admin user
```
python manage.py createsuperuser
```

## Use the admin panel
```
http://127.0.0.1:8000/admin/
```

# Database Interaction / QuerySets

Once you have created your data models, Django gives you a free API to interact with them.

`objects` is the default manager of every model that retrieves all objects in the database. 
However, you can also define custom managers for your models.

## Interact with Database-Api

### start Django shell
```bash
python manage.py shell
```

### Use DB Api 

Create a new Blog Post

```python
from django.contrib.auth.models import User
from blog.models import Post
user = User.objects.get(username='admin')
post = Post(title='Another post',slug='another-post',body='Post body.',author=user)
post.save()
```

Retrieving objects:

```python
all_posts = Post.objects.all()
```

Filter objects

```python
Post.objects.filter(publish__year=2020, author__username='admin')
# is the same as
Post.objects.filter(publish__year=2020) \
            .filter(author__username='admin')
```

Filter and exclude objects
```python
Post.objects.filter(publish__year=2020).exclude(title__startswith='Why')
```

Order a set of objects
```python
Post.objects.order_by('title')
```

Delete objects
```python
post = Post.objects.get(id=1)
post.delete()
```

## Model Managers

There are two ways to add or customize managers for your models: 
* you can add extra manager methods to an existing manager
* create a new manager by modifying the initial QuerySet that the manager returns. 

> The first method provides you with a QuerySet API such as `Post.objects.my_manager()`
> The latter provides you with `Post.my_manager.all()`. 
>The manager will allow you to retrieve posts using `Post.published.all()`