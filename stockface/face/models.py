#coding:utf-8
from __future__ import unicode_literals
from django.db import models
from pymongo import MongoClient
from collections import OrderedDict

import datetime
import time
import sys



# Create your models here.

class Stick(object):
    """
    蜡烛图节点
    """
    def __init__(self, _date, _price, _amount=0):
        self.date = _date
        self.open = _price
        self.high = _price
        self.low = _price
        self.close = _price
        self.amount = _amount
        self.counter = 1

    def change_price(self, _price, _amount=0):
        if _price > self.high:
            self.high = _price

        if _price < self.low:
            self.low = _price

        self.close = _price
        self.counter = self.counter + 1
        self.amount = self.amount + _amount

    def __str__(self):
        return "%s\t%.2f\t%.2f\t%.2f\t%.2f\n" % (self.date, self.open, self.high, self.low, self.close)

    def get_dict(self):
        r = OrderedDict()
        r["date"] = self.date
        r["timestamp"] = time.mktime(time.strptime(self.date,'%Y-%m-%d %H:%M:%S')) * 1000
        r["open"] = self.open
        r["high"] = self.high
        r["low"] = self.low
        r["close"] = self.close
        r["amount"] = self.amount
        r["counter"] = self.counter
        return r

    def get_list(self):
        r = []
        r.append(self.date)
        r.append(time.mktime(time.strptime(self.date,'%Y-%m-%d %H:%M:%S')) * 1000)
        r.append(self.open)
        r.append(self.high)
        r.append(self.low)
        r.append(self.close)
        r.append(self.amount)
        r.append(self.counter)
        return r


class LineData(object):
    """
    k线对应的数据
    """
    def __init__(self):
        self.__data = OrderedDict()

    def insert_days(self, data):
        ctime = data.get("ctime", "")
        price = float(data.get("price", 0.0))
        amount = float(data.get("amount", 0.0))
        if not ctime:
            print "error"
            return "error"
        cur_date = ctime.split(' ')[0]
        if cur_date not in self.__data:
            self.__data[cur_date] = Stick(cur_date, price, amount)
        else:
            self.__data[cur_date].change_price(price, amount)

    def get_data(self):
        r = []
        for (k, v) in self.__data.items():
            r.append(v.get_dict())
        #return r
        return sorted(r, cmp=lambda x, y: cmp(x["timestamp"], y["timestamp"]))
        

class StockModule(object):

    def __init__(self):
        self.db_client = MongoClient('mongodb://127.0.0.1:27018/')
        self.db_table = self.db_client["huangye"]
        self.linedata = LineData()

    def __find(self, table_name, query={}):
        return self.db_table[table_name].find(query)#.limit(100000)

    def __save(self, table_name, data={}):
        data["__TIME_STAMP__"] = time.time()
        data = OrderedDict(sorted(data.items(), key=lambda item: item[0]))
        self.db_table[table_name].save(data)
    
    def get_all_btc_cny(self, type, limits=1024):
        """
        type: 1d, 12h, 1m ...
        btccny 获取k线数据
        """
        r = []
        print "type", type
        for item in self.__find("klines", {"type":type}):
            item.pop("_id")
            r.append(item)
        ret = sorted(r, cmp=lambda x, y: cmp(x["timestamp"], y["timestamp"]))
        if limits == 0:
            return ret
        elif len(r) <= limits:
            return ret
        else:
            #出最近limits条数据
            r2 = []
            for i in range(len(r) - limits, len(r)):
                r2.append(r[i])
            return r2

