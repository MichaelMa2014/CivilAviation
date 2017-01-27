from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from json import loads
from json import dumps
from Map.models import Record
import time

# Create your views here.
# 渲染index主页
def index(request):
    return render(request, 'index.html')

# 渲染航线页
def airline(request):
    return render(request, 'airline.html')

# 将时分秒时间转为timestamp
def HMS2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))


# 数据请求接口
def getDataByDate(request, date):
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
#    cursor = Record.objects.filter(timestamp_gte=HMS2ts(f_second)).filter(timestamp_lte=HMS2ts(f_second)).distinct()
    #测试用
    cursor = Record.objects.filter(timestamp_gte=10000000).filter(timestamp_lte=1495103103).distinct()
    ret = []
    for record in cursor:
        ret.append(record)
    return HttpResponse(dumps(ret),content_type='application/json')


# 获取实时数据并存入数据库
def getrealtime():
    data = request.urlopen(url='http://219.224.134.225:5050/real-time')
    dataList = loads(data.read().decode('utf-8'))
    cnt = 1
    for item in dataList:
        newRecord = Record(item)
        try:
            newRecord.save()
            cnt += 1
        except:
            print("A Record failed to be saved")
    print(str(cnt) + " Record(s) has been saved")

getrealtime()