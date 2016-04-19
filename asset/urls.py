from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /device/
    url(r'^$', views.asset, name='asset'),
    url(r'^design$', views.design, name='design'),
    url(r'^entering$', views.entering, name='entering'),
]
