import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cc.settings")
from device.models import *
f = open('niplist','r')
while 1:
    line = f.readline()
    if line != '':
        d_name = line.split()[0]
        d_ip = line.split()[1]
        d_area = line.split()[2]
        d_city = line.split()[3]
        n_name = '-'.join((d_name.split('-')[0], d_name.split('-')[1]))
        no = Node.objects.get(node_name=n_name)
        d_status = 'online'
        if '6X' in d_name:
            d_mod = 'S6700'
        elif '6Y' in d_name:
            d_mod = 'CE5800'
        elif '6P' in d_name:
            d_mod = 'H3C5800'
        else:
            d_mod = 'unknow'
        if '6Z' in d_name:
            d_mod = 'IPMI'
            d_status = 'offline'
        no.device_set.create(device_name=d_name,device_mod=d_mod,device_ip=d_ip,device_status=d_status)
    else:break
f.close()
