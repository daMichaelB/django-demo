from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9  # relevance of post app within our website

    def items(self):
        """
        By default, Django calls the get_absolute_url() method on each object to retrieve its URL.
        """
        return Post.published.all()

    def lastmod(self, obj):
        """
        The lastmod method receives each object returned by items() and returns the last time the object was modified
        """
        return obj.updated
