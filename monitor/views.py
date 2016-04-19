#coding:utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
from graph import *
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def uplinkflow(request):
    node_all = Node.objects.all()
    curpage = Paginator(node_all, 7)
    node_all = curpage.page(1)
    pagenumber = 1
    if request.GET.get('page'):
        pagenumber = request.GET.get('page')
        node_all = curpage.page(pagenumber)
        pagenumber = int(pagenumber)
    return render(request, 'uplinkflow.html', {'node_all': node_all, 'curpage': curpage, 'pagenumber': pagenumber})

@login_required
def uplinkflownode(request, nodename):
    timerange = 'None'
    if request.GET.get('timerange'):
        timerange = request.GET.get('timerange')
    node = Node.objects.get(node_name=nodename)
    imgfile = 'None'
    if node.device_set.filter(device_role='CSW').count():
        CSWname = node.device_set.get(device_role="CSW").device_name
        imgfile = total_flow_graph(nodename, CSWname, timerange)
        print imgfile
    return render( request, 'uplinkflownode.html', {'nodename': nodename,'imgfile': imgfile})   
