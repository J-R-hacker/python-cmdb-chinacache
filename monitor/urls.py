from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /device/
    url(r'^uplinkflow$', views.uplinkflow, name='uplinkflow'),
    url(r'^uplinkflow/(?P<nodename>\w+-\w+)$', views.uplinkflownode, name='uplinkflownode'),
]
