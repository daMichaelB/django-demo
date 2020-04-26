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
* pw: xAJ4MuWecge3bbA

## Django authentication views

