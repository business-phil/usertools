from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view$', views.view, name='view-page'),
    url(r'^create$', views.create, name='create-user'),
    url(r'^login$', views.login, name='login'),
]
