# encoding=utf8
from django.shortcuts import render
from django.views import generic
import urllib.request, urllib.parse,ssl,sys
from django.utils import timezone
from django.http import HttpResponseRedirect
from .models import ShockList,shock_trade,User
from django.urls import reverse
import json
from django.contrib.auth import authenticate,login,logout
import random
# Create your views here.
import django

# host = 'https://ali-stock.showapi.com'
# path = '/real-stockinfo'
# appcode = '196e7cf84aa74bbabe4361fae5f079a6'
#
# querys = "code=600887&needIndex=1&need_k_pic=1"
# bodys = {}
# url = host + path + '?' + querys
# request=urllib.request.Request(url)
# request.add_header('Authorization', 'APPCODE ' + appcode)
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
# response = urllib.request.urlopen(request,context=ctx)
# content = json.loads(response.read())
# if (content):
#     print (content)

host = 'https://ali-stock.showapi.com'
appcode = '6f556175d4c1452bb2b39dae0c68ab1a'
class IndexView(generic.ListView):
    template_name = 'shock/index.html'
    context_object_name = 'shock_set'
    def get_queryset(self):
        shock_set=ShockList.objects.all().reverse()[3000:3835]
        self.request.session['shock_set']=shock_set
        return shock_set

def individual(request):
    user = User.objects.get(pk=request.user.id)
    trade_set=user.shock_trade_set.all()
    path='/batch-real-stockinfo'
    querys=''
    i=0
    for i in range(trade_set.count()-1):
        trade_set[i].code_str+'%2C'+querys
    #querys='stocks='+querys+trade_set[i].code_str
    querys='needIndex=0&stocks='+querys+trade_set[i].code_str
    content=connect_shock(host,path,appcode,querys)
    nowcontent=content['showapi_res_body']['list']
    for trade in trade_set:
        for now in nowcontent:
            if now['code']==trade.code:
                trade.now_price=float(now['nowPrice'])
                trade.profit=(trade.now_price-trade.cost)*trade.num
    for trade in trade_set:
        if trade.now_price==0:
            trade.now_price=trade.cost
            trade.profit=(trade.now_price-trade.cost)*trade.num
    return render(request,'shock/individualInfo.html',{'individualInfo':trade_set})

def acceptInfo(request):
    if request.POST['begin_time'] and request.POST['end_time'] and (request.POST['shock_name'] or request.POST['shock_code']):
        path = '/sz-sh-stock-history'
        if request.POST['shock_code']:
            code=request.POST['shock_code']
        else:code=getCodefromName(request.POST['shock_name'])
        querys = 'begin='+request.POST['begin_time']+'&end='+request.POST['end_time']+'&code=' + code
        content = connect_shock(host, path, appcode, querys)
        historyInfo = content['showapi_res_body']['list']
        return render(request, 'shock/index.html', {'historyInfo': historyInfo})
    elif request.POST['shock_name'] or request.POST['shock_code']:
        path = '/name-to-stockinfo'
        if request.POST['shock_name']:
            code=getCodefromName(request.POST['shock_name'])
        else:code=request.POST['shock_code']
        return HttpResponseRedirect(reverse('detail',args=(code,)))
    else:return HttpResponseRedirect(reverse('index'))

def connect_shock(host,path,appcode,querys):
    url = host + path + '?' + querys
    print(url)
    shock_request = urllib.request.Request(url)
    shock_request.add_header('Authorization', 'APPCODE ' + appcode)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(shock_request, context=ctx)
    content = json.loads(response.read())
    return content

def detailInfo(request,code):
    path = '/real-stockinfo'
    if code<1000:
        querys = "needIndex=1&need_k_pic=1&code="+str(code).zfill(5)
    else:querys = "needIndex=1&need_k_pic=1&code="+str(code).zfill(6)
    #print(connect_shock(host,path,appcode,querys)['showapi_res_body'])
    content=connect_shock(host,path,appcode,querys)['showapi_res_body']
    detailContent=content['stockMarket']
    imageUrl=content['k_pic']
    #print(imageUrl)
    detailcontext={'detailContent':detailContent,'imageUrl':imageUrl,'code':str(code).zfill(6)}
    request.session['detailcontext']=detailcontext
    return render(request,'shock/index.html',detailcontext)
    #return render(request,'shock/index.html')

def getCodefromName(name):
    q=ShockList.objects.get(name=name)
    return q.code
def getNamefromCode(code):
    q=ShockList.objects.get(code=code)
    return q.name

def loginInfo(request):
    username=request.POST['username']
    password=request.POST['password']
    user=authenticate(username=username,password=password)
    if user is not None:
        message='登录成功'
        login(request,user)
    else:message='用户名或密码错误'
    return render(request,'shock/index.html',{'message':message})

def loginexit(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def sell_or_buy(request,code):
    user=User.objects.get(pk=request.user.id)
    trade,tup=user.shock_trade_set.get_or_create(code=code)

    trade.num+=int(request.POST['buy_num'])-int(request.POST['sell_num'])
    trade.shock_name=getNamefromCode(code)
    trade.code_str=request.session['detailcontext']['detailContent']['market']+code
    trade.cost=float(request.session['detailcontext']['detailContent']['nowPrice'])
    message='操作成功'
    if trade.num<0:
        trade.num+=int(request.POST['sell_num'])-int(request.POST['buy_num'])
        message='股票数量不足'
    trade.save()
    request.session['detailcontext'].update({'erromessage':message})
    return render(request,'shock/index.html',request.session['detailcontext'])

class RegisterView(generic.ListView):
    template_name = 'shock/register.html'
    context_object_name = 'register'
    def get_queryset(self):
        return []

def createAccount(request):
    username = request.POST['username']
    password = request.POST['password']
    if User.objects.filter(username=username).exists():
        return render(request,'shock/register.html',{'message':'用户名已存在'})
    else:
        user=User.objects.create_user(username=username,password=password)
        login(request,user)
        return render(request,'shock/index.html')







