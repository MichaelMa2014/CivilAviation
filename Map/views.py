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
    print('function is called ',date)
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = Record.objects.filter(timestamp__gte=HMS2ts(f_second)).filter(timestamp__lte=HMS2ts(l_second)).only('lat','lon','num1', 'flight').distinct()
    ret = []
    for record in cursor:
        d = {}
        for attr in ['airline_code2', 'lon', '_id', 'airport_icao_code', 'num5', 'typecode', 'first_in', 'airline_code1', 'lat', 'flight', 'height', 'num3', 'airport_dep', 'timestamp', 'idshex', 'str1', 'num2', 'last_modify', 'zone_range', 'airport_arr', 'num1', 'num4', 'fid']:
            if record.__dict__[attr]:
                d.update({attr:record.__dict__[attr]})
        ret.append(d)
    ret = ret[:10]
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
