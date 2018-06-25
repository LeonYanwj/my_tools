from django.shortcuts import render,redirect,HttpResponse
from managehost import models
import json
# Create your views here.

def createhost(request):
    hostlist = [
        "192.168.2.21",
        "192.168.2.22",
        "192.168.2.23",
        "192.168.2.24",
        "192.168.2.25",
        "192.168.2.26",
        "192.168.2.27",
        "192.168.2.28",
        "192.168.2.29",
        "192.168.2.30",
        "192.168.2.31",
        "192.168.2.32",
        "192.168.2.33",
        "192.168.2.34",
        "192.168.2.35",
        "192.168.2.36",
        "192.168.2.37",
        "192.168.2.38",
        "192.168.2.39",
        "192.168.2.40",
        "192.168.2.245",
        "192.168.2.246",
        "192.168.2.247",
        "192.168.2.248",
        "192.168.2.249",
        "192.168.2.250",
        "192.168.2.251",
        "192.168.2.252",
    ]
    count = 1
    for ip in hostlist:
        models.HostInfo.objects.create(
            nickname="dmz%s"%count,
            ipaddr=ip,
            hosttype_id=1,
        )
        count += 1
    return HttpResponse("ok")

def login(request):
    response = {'status': False,'error': None,'message': ''}
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        userobj = models.UserInfo.objects.filter(username=u,password=p).first()
        if userobj:
            request.session['msg'] = {'username': u,'password': p}
            response['status'] = True
            response['message'] = '登录成功'
        else:
            response['status'] = False
            response['message'] = '登录失败'
            response['error'] = '用户名或者密码错误'
        return HttpResponse(json.dumps(response))
    return render(request,'login.html')


def home(request):
    if request.session.get('msg'):
        return render(request,'home.html')
    return redirect('/login.html')

def form_component(request):
    return render(request,'form_component.html')