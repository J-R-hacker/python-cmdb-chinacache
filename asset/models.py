from django.db import models
from device.models import *
# Create your models here.

class unitype(models.Model):
    unitype = models.CharField(max_length=50)
    manu = models.CharField(max_length=200)
    GiElectNum = models.CharField(max_length=50)
    XGLightNum = models.CharField(max_length=50)
    def __unicode__(self):
        return self.unitype