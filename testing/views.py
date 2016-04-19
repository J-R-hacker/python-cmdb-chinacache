from django.shortcuts import render

# Create your views here.


def langing(request):
    return render(request, 'langing.html')

def admin(request):
    return render(request, 'admin.html')

def test(request):
    return render(request, 'test.html')