from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /device/
    url(r'^$', views.info, name='info'),
    url(r'^networkinfo$', views.networkinfo, name='network'),
    url(r'^networkinfo/(?P<nodename>\w+-\w+)$', views.networkinfo, name='networkinfo'),
    url(r'^(?P<devname>\w+-\w+-\w+-\w+)$', views.device, name='device'),
]
