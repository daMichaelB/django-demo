from django.urls import path

from . import views

app_name = 'pages'  # namespace for django to differentiate urls with same name in different apps

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about')
]