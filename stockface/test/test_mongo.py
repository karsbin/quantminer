#coding:utf-8
from pymongo import MongoClient
from collections import OrderedDict

import datetime
import json
import copy
import time
import sys


class DbOp(object):
    def __init__(self):
        self.db_client = MongoClient('mongodb://127.0.0.1:27018/')
        self.db_table = self.db_client["huangye"]

    def __del__(self):
        self.db_client.close()

    def insert(self, r):
        self.db_table["test"].save(r)

    def update(self, rold, rnew=0):
        #self.db_table["test"].update(rold)
        self.db_table["test"].update(rold, rnew)

    def remove(self, r):
        self.db_table["test"].remove(r)


dbop = DbOp()
for line in open("test.json", "r"):
    line = line.strip()
    #dbop.remove(json.loads(line))
    r = json.loads(line)
    newr = copy.copy(r)
    newr["add"] = 1
    dbop.update(r, newr)




