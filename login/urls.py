from django.conf.urls import url
from . import views
 

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^login/$', views.login),
    url(r'^passport$', views.passport),
    url(r'^registe$', views.registe),
]