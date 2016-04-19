#coding:utf-8
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def info(request):
    print request
    node_all = Node.objects.all()
    curpage = Paginator(node_all, 9)
    node_all = curpage.page(1)
    pagenumber = 1
    if request.GET.get('page'):
        pagenumber = request.GET.get('page')
        node_all = curpage.page(pagenumber)
        pagenumber = int(pagenumber)
    return render(request, 'info.html', {'node_all': node_all, 'curpage': curpage, 'pagenumber': pagenumber})

@login_required
def networkinfo(request, nodename=u'所有设备'):
    m = Manu.objects.all()
    print m
    if nodename == u'所有设备':
        device_all = Device.objects.all()
    else:
        node = Node.objects.get(node_name=nodename)
        device_all = node.device_set.order_by("-device_status")
    #paging
    curpage = Paginator(device_all, 8)
    device_all = curpage.page(1)
    pagenumber = 1
    if request.GET.get('page'):
        pagenumber = request.GET.get('page')
        device_all = curpage.page(pagenumber)
        pagenumber = int(pagenumber)
    #页号再分片
    onepagemax = 7
    pagemax = curpage.page_range[-1]
    if pagenumber < onepagemax:
        if pagemax < onepagemax:
            page_range = [i for i in range (1, pagemax + 1)]
        else:
            page_range = [i for i in range (1, onepagemax + 1)]
    elif pagenumber > (pagemax - onepagemax): 
        page_range = [i for i in range ((pagemax - onepagemax), (pagemax + 1))]
    else:
        startpage = pagenumber - onepagemax/2 - 1
        endpage = pagenumber + onepagemax/2
        page_range = [i for i in range (startpage, endpage)]
    return render(request, 'networkinfo.html', {'nodename':nodename, 'device_all':device_all, 
                                                'page_range':page_range, 'pagenumber':pagenumber,
                                                'pagemax': pagemax, 'm': m,
                                                })

@login_required
def device(request, devname):
    device = Device.objects.get(device_name=devname)
    ip = device.device_ip
    return render(request, 'device.html')
