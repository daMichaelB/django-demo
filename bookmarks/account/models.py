from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Define a many to many relationship of the user user model with itself - For a FOLLOWING System
user_model = get_user_model()
# User Model get's a new attribute 'following'
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers',
                                                            symmetrical=False)
                        )  # symmetrical=False: if I follow you, it doesn't mean that you automatically follow me


class Profile(models.Model):
    """
    Best way to extend the Django-User model is to create a Profile that has a one-to-one relationship to it.

    In order to keep your code generic, use the get_user_model() method to retrieve the user model and the
    AUTH_USER_MODEL setting to refer to it when defining a model's relationship with the user model, instead of
    referring to the auth user model directly.
    """
    # CASCADE: Delete profile, if user was deleted
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'
