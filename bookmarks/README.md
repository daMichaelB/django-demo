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

# Bookmarklets

> A **bookmarklet** is a bookmark stored in a web browser that contains JavaScript code to extend the browser's 
> functionality. When you click on the bookmark, the JavaScript code is executed on the website being displayed 
> in the browser. This is very useful for building tools that interact with other websites.

Since the JavaScript code will be stored as a bookmark, you will not be able to update it later. 
This is an important drawback that you can solve by implementing a launcher script to load the actual 
JavaScript bookmarklet from a URL. Your users will save this launcher script as a bookmark, and you will be able to 
update the code of the bookmarklet at any time. This is the approach that you will take to build your bookmarklet.

See: bookmarklet_launcher.js (jQuery)

# Thumbnails

Install the package and add it to `settings.py`

```bash 
pip install easy-thumbnails==2.7
```

```python 
# settings.py
INSTALLED_APPS = [    
    # ...    
    'easy_thumbnails',
]
```

The **easy-thumbnails** application offers you different ways to define image thumbnails. 
The application provides a `{% thumbnail %}` template tag to generate thumbnails in templates and a custom 
`ImageField` if you want to define thumbnails in your models. 

# AJAX actions with jQuery

## Ajax Definition

**AJAX** comes from Asynchronous JavaScript and XML, encompassing a group of techniques to make 
asynchronous HTTP requests. 
It consists of sending and retrieving data from the server asynchronously, without reloading the whole page. 

> Instead of requesting a whole template the response for the request can only be a small JSON/Text

Despite the name, XML is not required. You can send or retrieve data in other formats, such as JSON, HTML, or 
plain text.

> You will need to add the AJAX functionality to your image detail template. In order to use jQuery in your templates, 
> you will include it in the base.html template of your project first.

Add it to the template:

```
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script>
    $(document).ready(function(){
      {% block domready %}
      {% endblock %}
    });
  </script>
```

You load the jQuery framework from Google's CDN. You can also download jQuery from https://jquery.com/ and 
add it to the static directory of your application instead.

> we add a django template block called domready --> here templates (that extend base.html) can inject JS

You add a `<script>` tag to include JavaScript code. `$(document).ready()` is a jQuery function that takes a 
handler that is executed when the Document Object Model (DOM) hierarchy has been fully constructed. The DOM is 
created by the browser when a web page is loaded, and it is constructed as a tree of objects. By including your 
code inside this function, you will make sure that all HTML elements that you are going to interact with are loaded 
in the DOM. Your code will only be executed once the DOM is ready.

> The examples in this chapter include JavaScript code in Django templates. 
> The preferred way to include JavaScript code is by loading .js files, which are served as static files, 
> especially when they are large scripts.

## CSRF with AJAX

Once CSRF protaction is active, Django checks for a CSRF token in all `POST` requests. 
Until now we used the `{% csrf_token %}` whenever we sent `POST` requests.

However, it is a bit inconvenient for AJAX requests to pass the CSRF token as POST data with every POST request. 
Therefore, Django allows you to set a custom X-CSRFToken header in your AJAX requests with the value of the CSRF token.

In order to include the token in all requests, you need to take the following steps:
* Retrieve the CSRF token from the csrftoken cookie, which is set if CSRF protection is active
* Send the token in the AJAX request using the X-CSRFToken header

## AJAX Paginatino with infinite scroll

Infinite scroll is achieved by loading the next results automatically when the user scrolls to the bottom of the page.