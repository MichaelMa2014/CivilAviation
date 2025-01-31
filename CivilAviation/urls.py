"""CivilAviation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Map import views as map_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', map_views.index),
    url(r'^airline$', map_views.airline, name='airline'),
    url(r'^getDataByDate/(\d+-\d+-\d+)', map_views.getDataByDate, name = 'getdatabydate'),
    url(r'^getDataByRect/([-]?\d+,[-]?\d+,[-]?\d+,[-]?\d+,\d+)', map_views.getDataByRect, name='getdatabyrect'),
    url(r'^getDataByID/(.*)', map_views.getDataByID, name = 'getdatabyid'),
    url(r'^getRouteByID/(.*)',map_views.getRouteByID, name = 'getroutebyid'),
    url(r'^getInfoByID/(.*)', map_views.getInfoByID, name='getinfobyid'),
]
