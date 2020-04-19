from django.urls import path
from . import views

app_name = 'blog'

# TODO: Check: does Django only define the endpoints here and we have to switch POST/GET/PUT/DELETE inside the view??
urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    # <slug:post> to specifically match a slug.
    # see also: https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]