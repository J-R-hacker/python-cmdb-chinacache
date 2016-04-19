from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /device/
    url(r'^langing$', views.langing, name='langing'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^$', views.test, name='test'),
]
