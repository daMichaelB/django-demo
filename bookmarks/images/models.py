from django.db import models
from django.utils.text import slugify

from django.conf import settings


class Image(models.Model):
    """
    Database indexes improve query performance. Consider setting db_index=True for fields that you
    frequently query using filter(), exclude(), or order_by(). ForeignKey fields or fields with
    unique=True imply the creation of an index. You can also use Meta.index_together or Meta.indexes
    to create indexes for multiple fields.
    """
    # CASCADE: delete images if a user is deleted!
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)  # for SEO friendly URLS
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True, db_index=True)  # create a DB index for this field to search fast!!

    # many to many relationship: one user can like several images and one images can be liked by several users
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
