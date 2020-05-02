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

# Views

A Django view is just a Python function that receives a web request and returns a web response. 
All the logic to return the desired response goes inside the view.

### Template Tags

Template tags control the rendering of the template and look like `{% tag %}`

You can see all built-in template tags and filters at https://docs.djangoproject.com/en/3.0/ref/templates/builtins/.

### Templates

`{% load static %}` tells Django to load the static template tags that are provided by the `django.contrib.staticfiles`

---

After loading them, you are able to use the `{% static %}` template tag throughout this template. 
With this template tag, you can include the static files, such as the blog.css

---

`{% block %}` tags. These tell Django that you want to define a block in that area. 
Templates that inherit from this template can fill in the blocks with content. 
You have defined a block called `title` and a block called `content`

---

With the `{% extends %}` template tag, you tell Django to inherit from the `blog/base.html`

### Class Based Views

```python
# function based view
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

```python
# class based view
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
```

> Class-based views offer advantages over function-based views for some use cases. 
>They have the following features:          
> * Organizing code related to HTTP methods, such as GET, POST, or PUT, in separate methods, instead of using conditional branching
> * Using multiple inheritance to create reusable view classes (also known as mixins)

# Forms

Django comes with two base classes to build forms:
* **Form**: Allows you to build standard forms
* **ModelForm**: Allows you to build forms tied to model instances

# Tags

Integrating a third-party Django tagging application. 
* **django-taggit** is a reusable application that primarily offers you a Tag model and a manager to easily add tags to any model.

> Tags allow you to recommend users similar topics (topics with same tags)

# Custom Template Tags

Django offers a variety of template tags, such as `{% if %}` or `{% block %}`.
Here is a list of all available template tags: https://docs.djangoproject.com/en/3.0/ref/templates/builtins/.

Django provides the following helper functions that allow you to create your own template tags in an easy manner:
 * **simple_tag**: Processes the data and returns a string
 * **inclusion_tag**: Processes the data and returns a rendered template

### Example

Create a folder `templatetags` inside your app folder. 

```python
#blog_tags.py
from django import template
from ..models import Post
register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()
```

Now append the following tag inside your `*.html`:
```
{% load blog_tags %}
```

And now we can use our **custom template** inside the `html`:

```{% total posts %}```

> The power of custom template tags is that you can process any data and add it to any template regardless of the 
> view executed.

# Custom Template Filters

Django has a variety of built-in template filters that allow you to alter variables in templates. 
These are Python functions that take one or two parameters, 
the value of the variable that the filter is applied to, and an optional argument. 
They return a value that can be displayed or treated by another filter.

```python
# Filter withouth argument
{{ variable |my_filer }}

# Filter with argument
{{ variable |my_filter:"foo" }}

# Apply many filters one after another
{{ variable |filter1:"foo"|filter2  }}
```

More information: https://docs.djangoproject.com/en/3.0/howto/custom-template-tags/#writing-custom-template-filters.

# Adding a sitemap

> Why? For SEO! A sitemap is a .xml that tells search engines the pages of your web sites and their relevance.

The Django sitemap framework depends on **django.contrib.sites**. It allows us to link objects to particular websites.

`INSTALLED_APPS` in `settings.py` need to be extended with

```python
    ...
    'django.contrib.sites',
    'django.contrib.sitemaps'
```

then: `python manage.py migrate`

The sitemap will be added to the global `urls.py` with the URL `http://127.0.0.1:8000/sitemap.xml`.
The generated `XML` will look like:

```XML
<urlset>
<url>
<loc>
http://example.com/blog/2020/4/24/first-markdown-post/
</loc>
<lastmod>2020-04-24</lastmod>
<changefreq>weekly</changefreq>
<priority>0.9</priority>
</url>
<url>
<loc>
http://example.com/blog/2020/4/19/another-guitar-post/
</loc>
<lastmod>2020-04-19</lastmod>
<changefreq>weekly</changefreq>
<priority>0.9</priority>
</url>
<url>
<loc>http://example.com/blog/2020/4/17/my-second-post/</loc>
<lastmod>2020-04-17</lastmod>
<changefreq>weekly</changefreq>
<priority>0.9</priority>
</url>
</urlset>
```

> The contained URLS point to `example.com`. This is the default **Site** that was generated by `django.contrib.sites`.
> We can adjust it in the admin-dashboard under **Sites**.

> Here, you can set the domain or host to be used by the site's framework and the applications that depend on it.

# PostgreSQL

We are currently using SQLite for your blog project. 
This is sufficient for development purposes. 
However, for a production environment, you will need a more powerful database, 
such as PostgreSQL, MariaDB, MySQL, or Oracle.

## Full text search

> Although Django is a database-agnostic web framework, it provides a module that supports part of the rich feature
> set offered by PostgreSQL, which is not offered by other databases that Django supports.

### Setup local Postgres with docker 

We will work with a docker image of Postgres:

```bash
docker pull postgres
```

```bash
# start the image
docker run --name docker-postgres -e POSTGRES_USER=blog -e POSTGRES_PASSWORD=blogpassword -e POSTGRES_DB=blog -v my_dbdata:/var/lib/postgresql/data -p 5432:5432 -d postgres
```

### Connect Django to the Postgres docker DB

```python
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "blog"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "blogpassword"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}
```

Then migrate the initial tables and create a new superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### Use Django's Postgres App

```python
INSTALLED_APPS = [
    ...
    'django.contrib.postgres',
]
```

### Perform Full Text Search

```python
# on one field (body)
from blog.models import Post
Post.objects.filter(body__search='keyword')
```

```python
# on several fields (title, body)
from blog.models import Post
from django.contrib.postgres.search import SearchVector

Post.objects.annotate(search=SearchVector('title', 'body')).filter(search='keyword')
```

> If you are searching for more than a few hundred rows, you should define a functional index that matches the search 
> vector you are using.

## OTHER Full Text Search Engines

You may want to use a full-text search engine other than from PostgreSQL. If you want to use Solr or Elasticsearch, 
you can integrate them into your Django project using Haystack. Haystack is a Django application that works as an 
abstraction layer for multiple search engines.

# Running the development server through HTTPS
The Django development server is not able to serve your site through HTTPS, since that is not its intended use
In order get that, we use the **RunServerPlus** from *django extensions*.

Install packages 
```bash 
pip install django-extensions
pip install werkzeug
pip install pyOpenSSL
```

Start the server

```bash
python manage.py runserver_plus --cert-file cert.crt
```

