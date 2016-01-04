#coding:utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

import json
import urllib
import urllib2
import httplib
import sys

from models import StockModule
from lib.common import *

stock_module = StockModule()

def get_all_btc_cny(request):
    type = request.GET.get("type", "1d")
    res = stock_module.get_all_btc_cny(type)
    return HttpResponse(json.dumps(res), content_type="application/json", charset="utf-8")

def btc_cny(request):
    type = request.GET.get("type", "1d")
    y = request.GET.get("y", "linear")
    if y == "log":
        y = "logarithmic"
    return render_to_response("btccny.html", {"type":type, "y":y})

# Create your views here.
def index(request):
    res = "hello"
    return HttpResponse(res)
