#coding:utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
# Create your views here.

def asset(request):
    return render(request, 'asset.html')

def design(request):
    return render(request, 'design.html')

def entering(request):
    hit = "nothing"
    nameinfo = "nothing"
    if request.GET.get("city") and request.GET.get("nodename") and  request.GET.get("area"):
        nodename = request.GET.get("nodename").upper()
        city = request.GET.get("city")
        area = request.GET.get("area")
        nameinfo = nodename
        if not Node.objects.filter(node_name=nodename).count():
            Node.objects.create(node_name=nodename, area=area, city= city)
            hit = "isok"
        else:
            hit = "ihave"
    elif request.GET.get("devicename") and request.GET.get("deviceip"):
        devicename = request.GET.get("devicename").strip().strip("\n")
        deviceip = request.GET.get("deviceip")
        nodeid = Node.objects.get(node_name=request.GET.get("belongnode")).id
        manuid = Manu.objects.get(dtype=request.GET.get("devicetype")).id
        nameinfo = devicename
        if not Device.objects.filter(device_name=devicename).count():
            Device.objects.create(device_name=devicename, device_ip=deviceip, node_id=nodeid, manu_id=manuid, device_status="online")
            hit = "isok"
        else:
            hit = "ihave"
    node = Node.objects.all()
    utype = Manu.objects.order_by("Manu")
    return render(request, 'entering.html', { "node": node, "utype": utype, "hit": hit, "nameinfo": nameinfo})
