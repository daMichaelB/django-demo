from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # <slug:post> to specifically match a slug.
    # see also: https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail')
]