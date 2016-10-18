# -*- coding: utf-8 -*-

import pymongo
from flask import Flask
from bson.code import Code

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

print("test start....")
date = "2016-06-10"
f_second = date + ' 00:00:00'
l_second = date + ' 23:59:59'

mapper = Code("""
                function() {
                    list = ["PVG", "PEK", "SHA", "CTU", "XMN", "SYX", "HGH", "CAN", "SZX", "HAK", "CKG", "NKG", "TYN",
                    "SHE", "KWE", "XIY", "YNT", "TNA", "NAY", "TAO", "SJW", "WUX", "CGO", "TSN", "XNN", "KMG", "JJN",
                    "CGQ", "LJG","FOC", "MFM", "CSX", "KHN", "HRB", "URC", "LHW", "ZUH", "BHY", "DLC", "XUZ", "HET",
                    "HFE", "KWL", "SWA", "WUH", "NGB", "DAT", "JUZ", "NNG", "YIW", "WNZ", "LYI", "NTG", "NNY", "DLU",
                    "HMI", "NAO", "CZX", "HLH", "DAX", "YNZ", "YNJ", "AQG", "ZYI", "JMU", "DSN", "MIG", "JNZ", "INC",
                    "JHG", "NDG", "HYN", "HLD", "JGN", "LYG", "HUZ", "AKU", "NBS", "YCU", "BFJ", "YBP", "YIH", "AAT",
                    "YTY", "XFN", "DDG", "LXA", "LUM", "CIF", "BAV", "WXN", "HIA", "UYN", "HTN", "TGO", "TVS", "KOW",
                    "NZH", "DYG", "BSD", "WEF", "LZH", "ZHA", "WEH", "JDZ", "CIH", "LLF", "KHG", "FUG", "LYA", "DIG",
                    "WUS", "AVA", "MDG", "SYM", "GYS", "HDG", "WUA", "KRL", "ZQZ", "LZO", "TXN", "ENH", "XIL", "CGD",
                    "YIC", "YIN", "KRY", "DCY", "HSN", "LCX", "JXA", "TNH", "JGS", "MXZ", "TCZ", "YKH", "DNH", "KGT",
                    "ZHY", "ZAT", "TEN", "JNG", "AOG", "HNY", "JZH", "HEK", "WNH", "ENY", "IQN", "CHG", "ACX", "JIC",
                    "GXH"]
                    if (list.indexOf(this.airport_dep)>=0 && list.indexOf(this.airport_dep)>=0) {
                        emit([this.airport_dep, this.airport_arr], 1)
                    }
                }
              """)

reducer = Code("""
                function(key, values) {
                    return Array.sum(values)
                }
               """)

result = mongo["trails_20160610"].inline_map_reduce(mapper, reducer)
print(result)
