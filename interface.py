#-*- coding: utf-8 -*-

import time
import json
import pymongo
from flask import Flask
from flask import request
from flask import url_for

app = Flask(__name__)

MONGOD_HOST = '219.224.134.213'
MONGOD_PORT = 27017

def _default_mongo(host=MONGOD_HOST, port=MONGOD_PORT, usedb='test'):
    # 强制写journal，并强制safe
    connection = pymongo.MongoClient(host=host, port=port, j=True, w=1)
    # db = connection.admin
    # db.authenticate('root', 'root')
    db = getattr(connection, usedb)
    return db
mongo = _default_mongo(usedb='flightradar')

collection_name = "all_trails"
daily_collection_name_prefix = "trails_"

def HMS2ts(date):
    return int(time.mktime(time.strptime(date, '%Y-%m-%d %H:%M:%S')))

@app.route('/')
def date_trails():
    # return url_for('date_trails')
    date = request.args.get("date") # '2016-07-01'

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}})
    results.extend([r for r in cursor])

    return json.dumps(results)


@app.route('/airline')
def airline_trails():
    date = request.args.get("date")
    airline_code1 = request.args.get("airline")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airline_code1": airline_code1})
    results.extend([r for r in cursor])


    return json.dumps(results)

@app.route('/flight')
def flight_trails():
    date = request.args.get("date")
    fid = request.args.get("flight")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "fid": fid})
    results.extend([r for r in cursor])


    return json.dumps(results)

@app.route('/dep')
def dep_trails():
    date = request.args.get("date")
    dep = request.args.get("dep")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_dep": dep})
    results.extend([r for r in cursor])


    return json.dumps(results)

@app.route('/dep-flight')
def dep_flight_trails():
    date = request.args.get("date")
    dep = request.args.get("dep")
    fid = request.args.get("flight")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "fid": fid, "airport_dep": dep})
    results.extend([r for r in cursor])

    return json.dumps(results)

@app.route('/arr')
def arr_trails():
    date = request.args.get("date")
    arr = request.args.get("arr")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_arr": arr})
    results.extend([r for r in cursor])

    return json.dumps(results)

@app.route('/arr-flight')
def arr_flight_trails():
    date = request.args.get("date")
    arr = request.args.get("arr")
    fid = request.args.get("flight")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "fid": fid, "airport_arr": arr})
    results.extend([r for r in cursor])

    return json.dumps(results)

@app.route('/dep-arr')
def dep_arr_trails():
    date = request.args.get("date")
    dep = request.args.get("dep")
    arr = request.args.get("arr")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    cursor = mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_dep": dep, "airport_arr": arr})
    results.extend([r for r in cursor])

    return json.dumps(results)

@app.route('/dep-arr-multi')
def dep_arr_trails_multi():
    dates = request.args.get("dates").split(",") # 2016-06-10,2016-06-11
    dep = request.args.get("dep")
    arr = request.args.get("arr")

    results = []
    for date in dates:
        f_second = date + ' 00:00:00'
        l_second = date + ' 23:59:59'
        daily_collection_name_prefix + date.replace("-", "")
        cursor = mongo[daily_collection_name_prefix + date.replace("-", "")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_dep": dep, "airport_arr": arr})
        results.extend([r for r in cursor])

    return json.dumps(results)


@app.route('/count')
def date_trails_count():
    date = request.args.get("date") # '2016-07-01'

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}}).count()



@app.route('/airline-count')
def airline_trails_count():
    date = request.args.get("date")
    airline_code1 = request.args.get("airline")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airline_code1": airline_code1}).count()



@app.route('/flight-count')
def flight_trails_count():
    date = request.args.get("date")
    fid = request.args.get("flight")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "fid": fid}).count()



@app.route('/dep-count')
def dep_trails_count():
    date = request.args.get("date")
    dep = request.args.get("dep")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_dep": dep}).count()



@app.route('/dep-flight-count')
def dep_flight_trails_count():
    date = request.args.get("date")
    dep = request.args.get("dep")
    fid = request.args.get("flight")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "fid": fid, "airport_dep": dep}).count()


@app.route('/arr-count')
def arr_trails_count():
    date = request.args.get("date")
    arr = request.args.get("arr")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_arr": arr}).count()


@app.route('/arr-flight-count')
def arr_flight_trails_count():
    date = request.args.get("date")
    arr = request.args.get("arr")
    fid = request.args.get("flight")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "fid": fid, "airport_arr": arr}).count()


@app.route('/dep-arr-count')
def dep_arr_trails_count():
    date = request.args.get("date")
    dep = request.args.get("dep")
    arr = request.args.get("arr")

    results = []
    f_second = date + ' 00:00:00'
    l_second = date + ' 23:59:59'
    return mongo[daily_collection_name_prefix + date.replace("-","")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_dep": dep, "airport_arr": arr}).count()


@app.route('/dep-arr-multi-count')
def dep_arr_trails_multi_count():
    dates = request.args.get("dates").split(",") # 2016-06-10,2016-06-11
    dep = request.args.get("dep")
    arr = request.args.get("arr")

    results = []
    for date in dates:
        f_second = date + ' 00:00:00'
        l_second = date + ' 23:59:59'
        daily_collection_name_prefix + date.replace("-", "")
        return mongo[daily_collection_name_prefix + date.replace("-", "")].find({"timestamp": {"$gte": HMS2ts(f_second), "$lte": HMS2ts(l_second)}, "airport_dep": dep, "airport_arr": arr}).count()

    return json.dumps(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
