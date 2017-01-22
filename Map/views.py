from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from json import loads
from Map.models import Record

# Create your views here.
# 渲染index主页
def index(request):
    return render(request, 'index.html')

# 渲染航线页
def airline(request):
    return render(request, 'airline.html')

# 数据请求接口
def getdata(request, time):
    return HttpResponse('yes')

data = request.urlopen(url='http://219.224.134.225:5050/real-time')
dataList = loads(data.read().decode('utf-8'))

for item in dataList[:5]:
    newRecord = Record(item)
    newRecord.save()
    print("A Record has been saved")