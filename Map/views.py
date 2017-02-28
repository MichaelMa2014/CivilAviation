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
# 根据日期获取数据
def getDataByDate(request, date):
    print('fetching data by data ',date)
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = Record.objects.filter(timestamp__gte=HMS2ts(f_second)).filter(timestamp__lte=HMS2ts(l_second)).only('lat','lon').distinct()
    ret = []
    for record in cursor:
        d = {}
        for attr in ['airline_code2', 'lon', '_id', 'airport_icao_code', 'num5', 'typecode', 'first_in', 'airline_code1', 'lat', 'flight', 'height', 'num3', 'airport_dep', 'timestamp', 'idshex', 'str1', 'num2', 'last_modify', 'zone_range', 'airport_arr', 'num1', 'num4', 'fid']:
            if record.__dict__[attr]:
                d.update({attr:record.__dict__[attr]})
        ret.append(d)
    return HttpResponse(dumps(ret),content_type='application/json')


# 根据经纬度以及缩放等级返回矩形框内的数据
# lngslats分别为sw,ne点的经纬度以及缩放等级
def getDataByRect(request, lngslats):
    lngslats = lngslats.split(sep=',')
    swlng,swlat,nelng,nelat,zoom = int(lngslats[0]),int(lngslats[1]),int(lngslats[2]),int(lngslats[3]),int(lngslats[4])
    print('request:getDataByRect:',swlng,swlat,nelng,nelat,zoom)
    cursor = Record.objects.filter(lat__gte=swlat, lon__gte=swlng, lat__lte=nelat, lon__lte=nelng).only('lat','lon','fid').distinct()[:300]
    ret = []
    cnt = 0
    for record in cursor:
        d = {}
        d.update({'lat':record.lat})
        d.update({'lon':record.lon})
        d.update({'id':record.fid})
        if not record._id:
            cnt += 1
        ret.append(d)
    return HttpResponse(dumps(ret), content_type='application/json')



def getDataByID(request, fid):
    print(fid)
    cursor = Record.objects.filter(fid__exact=fid)
    ret = []
    d = [123]
    for record in cursor:
        d = {}
        for attr in ['airline_code2', 'lon', '_id', 'airport_icao_code', 'num5', 'typecode', 'first_in',
                     'airline_code1', 'lat', 'flight', 'height', 'num3', 'airport_dep', 'timestamp', 'idshex', 'str1','num2', 'last_modify', 'zone_range', 'airport_arr', 'num1', 'num4', 'fid']:
            d.update({attr: record.__dict__[attr]})
    return HttpResponse(dumps(d), content_type='application/json')


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
