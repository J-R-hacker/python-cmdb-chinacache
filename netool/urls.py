from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /device/
    url(r'^$', views.netool, name='netool'),    
    url(r'^netcheck$', views.netcheck, name='netcheck'),

]
