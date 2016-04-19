from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /device/
    url(r'^$', views.subnet, name='subnet'),
    url(r'^insubnet$', views.insubnet, name='insubnet'),
    url(r'^add_insubnet$', views.addinsubnet, name='addinsubnet')
]