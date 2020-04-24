from django.urls import path
from . import views

app_name = 'blog'

# TODO: Check: does Django only define the endpoints here and we have to switch POST/GET/PUT/DELETE inside the view??
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    # You use a slug path converter to match the parameter as a lowercase string with ASCII letters or numbers,
    # plus the hyphen and underscore characters.
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    # path('', views.PostListView.as_view(), name='post_list'),
    # <slug:post> to specifically match a slug.
    # see also: https://docs.djangoproject.com/en/3.0/topics/http/urls/#path-converters.
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
]