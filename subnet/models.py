from django.db import models
from device.models import *
# Create your models here.

class Insubnet(models.Model):
    subnet_id = models.CharField(max_length=100)
    subnet_mask = models.CharField(max_length=100)
    subnet_status = models.CharField(max_length=50)
    subnet_fornode = models.CharField(max_length=100)
    def __unicode__(self):
        return self.subnet_id+"/"+self.subnet_mask
