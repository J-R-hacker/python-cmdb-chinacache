from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import *
from . import ipy
# Create your views here.

def subnet(request):
    return render(request, 'subnet.html')

def insubnet(request):
    insub_all = Insubnet.objects.all()
    return render(request, 'subnet.html', {'insub_all':insub_all })

def addinsubnet(request):
    insubnet_node = request.POST['insubnet_node']
    hosts = request.POST['insubnet_host']
    fip = Insubnet.objects.get(id=1).subnet_id
    nmask = ipy.get_mask(int(hosts))
    nip = ipy.ip_bin(fip)
    fid = ipy.next_id(nip, nmask)
    subnet_create = Insubnet.objects.create(subnet_id=ipy.ip_int(nip),subnet_mask=ipy.mask_len(nmask),subnet_status='used',subnet_fornode=insubnet_node)
    subnet_create.save()
    fristid = Insubnet.objects.get(id=1)
    fristid.subnet_id = fid
    fristid.save()
    insub_all = Insubnet.objects.all()
    return HttpResponseRedirect('insubnet')