from django.db import models

# Create your models here.
class Node(models.Model):
    node_name = models.CharField(max_length=50)
    area = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    def __unicode__(self):
        return self.node_name

class Manu(models.Model):
    Manu = models.CharField(max_length=80, null=True)
    dtype = models.CharField(max_length=100, null=True)
    def __unicode__(self):
        return self.Manu


class Device(models.Model):
    node = models.ForeignKey(Node)
    manu = models.ForeignKey(Manu)
    device_name = models.CharField(max_length=200)
    device_ip = models.CharField(max_length=50)
    device_role = models.CharField(max_length=50, default='ASW')
    device_status = models.CharField(max_length=200)
    device_uplinkoid = models.CharField(max_length=50, default='None')
    def __unicode__(self):
        return self.device_name

class Interface(models.Model):
    if_name = models.CharField(max_length=80, null=True)
    if_status = models.CharField(max_length=50, null=True)
    if_OID = models.CharField(max_length=50, null=True)
    if_role = models.CharField(max_length=50, null=True)
    if_desc = models.CharField(max_length=200, null=True)
    if_ip = models.CharField(max_length=50, null=True)
    device = models.ForeignKey(Device)
    def __unicode__(self):
        return self.if_name


