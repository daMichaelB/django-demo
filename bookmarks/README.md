# Django Auth framework

The authentication framework is located at `django.contrib.auth` and is used by other
`contrib` packages.

> When you create a new Django project using the `django-admin startproject ...` command, the authentication framework 
> is included in the default settings of your project.

It also consists of the two middleware classes found in the `MIDDLEWARE` setting of your project:
* **AuthenticationMiddleware:** Associates users with requests using sessions
* **SessionMiddleware:** Handles the current session across requests

> Middleware are classes with methods that are globally executed during the request or response phase.

The **authentication framework** includes the following models:
* User
* Group
* Permission

Note the difference between `authenticate()` and `login()`: 
* `authenticate()` checks user credentials and returns a User object if they are correct
* `login()` sets the user in the current session.

**Create Demo-User**
* name: testuser
* pw: K8sVnCNsmRzzwWW

## Django authentication views

Django includes several forms and views in the authentication framework that you can use right away.
Instead of coding those views with the User / Group and Permission model we can use those default Views:

* LoginView --> default template has to be in `templates/registration/login.html`
* LogoutView
* PasswordChangeView
* PasswordResetView
* ...

### Default view folder
In the folder `templates/registration/` django expects to find our views.

### `login_required` Decorator

We can decorate views with the `login_required` decorator of the authentication framework. 
The `login_required` decorator checks whether the current user is authenticated.

> if the user is not authenticated, it redirects the user to the login URL with the originally requested URL as a 
>GET parameter named `next` !!

# Serving media and static files

Add the following to the `settings.py`
```python
# To enable Django to serve media files uploaded by users with the development server
MEDIA_URL = '/media/'  # base URL used to serve the media files uploaded by users
# local path. You build the path dynamically relative to your project path to make your code more generic.
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
```

Now tell the Django development server to serve media files during development.

Extend the `urls.py`

```python
# only add this url in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

> Never serve your static files with Django in a production environment.

# Messages Framework

Inform the user with messages. It is located at: `django.contrib.messages`.
Messages are stored in a cookie by default (falling back to session storage).

They are displayed in the next request from the user. We can use the following functions:

```python
from django.contrib import messages
messages.error(request, 'Something went wrong')
        .success()
        .info()
        .warning()
        .debug()
        .add_message()
```

# Database

## Create Indexes for fast search

```python
Database indexes improve query performance. Consider setting db_index=True for fields that you
frequently query using filter(), exclude(), or order_by(). ForeignKey fields or fields with
unique=True imply the creation of an index. You can also use Meta.index_together or Meta.indexes
to create indexes for multiple fields.
```

## Many to Many relationship

```python
# many to many relationship: one user can like several images and one images can be liked by several users
# related_name allows to access the image from the user-object
users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
```