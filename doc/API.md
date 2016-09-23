# API

数据库使用 MongoDB 架设，使用 文件系统，每天的数据组成一个 document，因此查询时一定要指定日期。

URL 格式如下

IP地址／命令？参数名1＝参数值1&参数名2＝参数值2

命令有

- airline 指定飞机
- flight 指定航班
- dep 指定出发机场
- dep-flight 指定出发机场和航班
- arr 指定到达机场
- arr-flight 指定到达机场和航班
- dep-arr 指定出发机场和到达机场
- dep-arr-multi 指定多个日期的出发机场和到达机场
- <以上命令>-count 查询以上命令的结果的数量

参数有

- dates （格式为 YYYY-MM-DD,YYYY-MM,DD）
- date （格式为 YYYY-MM-DD)
- dep （出发机场三位编码）
- arr（到达机场三位编码）
- flight（航班号）

示例

```
http://219.224.134.225:5050/dep-arr-multi?dates=2016-06-10,2016-06-11&dep=PEK&arr=LAX
http://219.224.134.225:5050/dep-arr?date=2016-06-10&dep=PEK&arr=LAX
http://219.224.134.225:5050/dep-flight?date=2016-06-10&dep=PEK&flight=9f79b0e
```
