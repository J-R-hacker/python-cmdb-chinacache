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
        if not Node.objects.filter(node_name=n_name).count():
            node = Node.objects.create(node_name=n_name,area=d_area,city=d_city)           
    else:break
f.close()
