#coding=utf-8
import datetime
import time

def get_time_stamp(ctime):
    return time.mktime(time.strptime(ctime,'%Y-%m-%d %H:%M:%S')) * 1000

def get_datetime_by_timestamp(timestamp):
    dateArray = datetime.datetime.fromtimestamp(timestamp/1000)
    return dateArray

def get_datetime_str(cur_datetime):
    return "%d-%02d-%02d %02d:%02d:%02d" % (cur_datetime.year, cur_datetime.month\
            , cur_datetime.day, cur_datetime.hour, cur_datetime.minute, cur_datetime.second)

def cmp_datetime_by_day(dt1, dt2):
    tdt1 = datetime.datetime(dt1.year, dt1.month, dt1.day)
    tdt2 = datetime.datetime(dt2.year, dt2.month, dt2.day)
    return cmp(tdt1, tdt2)

def get_timestamp_by_datetime(cur_datetime):
    return time.mktime(cur_datetime.timetuple()) * 1000

def account_cmp(x, y):
    if x["timestamp"] == y["timestamp"]:
        if x.get("type") == "account_records":
            return -1
    return cmp(x["timestamp"], y["timestamp"])

