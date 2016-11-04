# API

数据库使用 MongoDB 架设，运行在 `219.224.134.213`，使用 Debian 文件系统
每天的数据为一个 document，命名为 `trails_YYYYMMDD`
API 服务器用 Flask 架设，运行在 `219.224.134.225`。API 服务器的代码为 `/interface.py`
可以在本地运行此 python 文件，然后访问 `localhost:5050/<command>`，同样可以获得数据

The database is constructed with MongoDB, hosted on `219.224.134.213`, with Debian as its file system.
Data from each day is put in separate collections, named as `trails_YYYYMMDD`.
The API server is constructed with Flask, hosted on `219.224.134.225`.
The code for the API server is `/interface.py`.
You can run this python and access `localhost:5050/<command>?<param>=<paramval>` to get data as well.

URL 格式如下

IP地址／命令？参数名1＝参数值1&参数名2＝参数值2

命令
command

- `airline` 指定飞机
- `flight` 指定航班
- `dep` 指定出发机场
- `dep-flight` 指定出发机场和航班
- `arr` 指定到达机场
- `arr-flight` 指定到达机场和航班
- `dep-arr` 指定出发机场和到达机场
- `dep-arr-multi` 指定多个日期的出发机场和到达机场
- `<all-above>-count` 查询以上命令的结果的数量
- `real-time` 实时数据

参数
param

- `dates` （格式为 YYYY-MM-DD,YYYY-MM-DD）
- `date` （格式为 YYYY-MM-DD)
- `dep` （出发机场三位编码）
- `arr`（到达机场三位编码）
- `flight`（航班号）

示例
examples

```
http://219.224.134.225:5050/dep-arr-multi?dates=2016-06-10,2016-06-11&dep=PEK&arr=LAX
http://219.224.134.225:5050/dep-arr?date=2016-06-10&dep=PEK&arr=LAX
http://219.224.134.225:5050/dep-flight?date=2016-06-10&dep=PEK&flight=9f79b0e
```
