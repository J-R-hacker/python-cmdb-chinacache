from django.shortcuts import render
from models import *
import re
from django.core.paginator import Paginator
from checknet import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def netcheck(request):
    device_all = "None"
    checkresult = {}
    if request.GET.get('seacrh'):
        search = request.GET.get('seacrh')#.strip()#.upper()
        if re.search(r'(\w\w\w\-\w\w\-\w\-\w\w\w)', search):
            search = re.search(r'(\w\w\w\-\w\w\-\w\-\w\w\w)', search).group()
            device_all = Device.objects.filter(device_name=search)
        else:
            seacrh = re.search(r'(\w\w\w\-\w\w)', search).group()
            node = Node.objects.get(node_name=search)
            device_all = node.device_set.order_by("-manu_id")
    hit = "None"
    if request.GET.get('checkdeviceid'):
        hit = "show"
        deviceid = request.GET.get('checkdeviceid')
        username = request.GET.get('username')
        device = Device.objects.get(id=deviceid)
        hostname = device.device_name
        ip = device.device_ip
        password = {"ccadmin": "Cc_npb_nb001",
        "xingchen.wang": "Wan9!@@%",
        }
        checkresult = checknet(username, password[username], hostname, ip)
    return render(request, 'netcheck.html', {"device_all": device_all, "hit": hit, "checkresult": checkresult})
@login_required
def netool(request):
    return render(request, 'netool.html')
