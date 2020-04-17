from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # author: This field defines a many-to-one relationship, meaning that each post is written by a user,
    # and a user can write any number of posts. For this field, Django will create a foreign key in the database
    # using the primary key of the related model. In this case, you are relying on the User model of the
    # Django authentication system.
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')

    class Meta:
        """
        The Meta class inside the model contains metadata. You tell Django to sort results by the publish field
        in descending order by default when you query the database. You specify the descending order using
        the negative prefix. By doing this, posts published recently will appear first.
        """
        ordering = ('-publish',)

    def __str__(self):
        return self.title
