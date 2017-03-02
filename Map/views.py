from django.shortcuts import render
from django.http import HttpResponse
from urllib import request
from json import loads
from json import dumps
from Map.models import Record
import time


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
    clng = (swlng + nelng) / 2
    clat = (swlat + nelat) / 2
    print(swlng,swlat,clng,clat,nelng,nelat);
    ret = []
    # 查询矩形框内的数据
    def querybyrect(llat, llng, glat, glng):
        cursor = Record.objects.filter(lat__gte=llat, lon__gte=llng, lat__lte=glat, lon__lte=glng).only('lat', 'lon','fid').distinct()[:70]
        for record in cursor:
            d = {}
            d.update({'lat': record.lat})
            d.update({'lon': record.lon})
            d.update({'id': record.fid})
            ret.append(d)

    # 左上
    querybyrect(clat, swlng, nelat, clng)
    # 右上
    querybyrect(clat, clng, nelat, nelng)
    # 左下
    querybyrect(swlat, swlng, clat, clng)
    # 右下
    querybyrect(swlat, clng, clat, nelng)
    print(len(ret))
    return HttpResponse(dumps(ret), content_type='application/json')


# 根据航班id返回航班数据
# fid为航班数据中的fid
def getDataByID(request, fid):
    print(fid)
    cursor = Record.objects.filter(fid__exact=fid)
    ret = []
    for record in cursor:
        d = {}
        for attr in ['airline_code2', 'lon', '_id', 'airport_icao_code', 'num5', 'typecode', 'first_in',
                     'airline_code1', 'lat', 'flight', 'height', 'num3', 'airport_dep', 'timestamp', 'idshex', 'str1','num2', 'last_modify', 'zone_range', 'airport_arr', 'num1', 'num4', 'fid']:
            d.update({attr: record.__dict__[attr]})
        ret.append(d)
    return HttpResponse(dumps(ret), content_type='application/json')


# 根据航班id返回航班的轨迹信息
# fid为航班数据中的fid
def getRouteByID(request, fid):
    # 根据时间戳排序是为了保证绘制轨迹的点是有序的
    cursor = Record.objects.filter(fid__exact=fid).order_by('timestamp')
    ret = []
    route = []
    for record in cursor:
        if len(route) != 0:
            olng = float(route[-1][0])
            olat = float(route[-1][1])
            dlng = float(record.lon)
            dlat = float(record.lat)
            if olng * dlng < 0 and abs(olng) + abs(dlng) > 180:
                # 跨越东西半球的轨迹
                # 计算两点间的精度差和纬度差
                difflng = 360 - (abs(olng) + abs(dlng))
                difflat = abs(olat - dlat)
                # 计算两点连线的以及经纬线构成的三角形的正切值
                tan = difflat / difflng
                if olng < 0:
                    # 从西半球飞往东半球
                    difflng = 180 - dlng
                    tanlat = tan * difflng
                    if olat > dlat:
                        # 从上往下飞
                        route.append([-180, dlat + tanlat])
                        ret.append(route)
                        route = []
                        route.append([180, dlat + tanlat])
                    else:
                        # 从下网上飞
                        route.append([-180, dlat - tanlat])
                        ret.append(route)
                        route = []
                        route.append([180, dlat - tanlat])
                else:
                    # 从东半球飞往西半球
                    difflng = 180 - olng
                    tanlat = tan * difflng
                    if olat > dlat:
                        # 从上往下飞
                        route.append([180, olat - tanlat])
                        ret.append(route)
                        route = []
                        route.append([-180, olat - tanlat])
                    else:
                        # 从下往上飞
                        route.append([180, olat + tanlat])
                        ret.append(route)
                        route = []
                        route.append([-180, olat + tanlat])
        route.append([record.lon, record.lat])
    ret.append(route)
    return HttpResponse(dumps(ret), content_type='application/json')


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


# 根据航班id和时间获取数据并存入数据库
def getroutebyid(id, date):
    data = request.urlopen(url='http://219.224.134.225:5050/flight?date=2016-06-09&dep=PEK&flight=9f79b0e')

    # data = request.urlopen(url='http://219.224.134.225:5050/flight?date='+date+'&flight='+id)
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
