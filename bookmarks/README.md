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