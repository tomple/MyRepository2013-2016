# -*- coding: utf-8 -*-
import datetime
import time

class DataRepository(object):
    def __init__(self):
        self.test = 'test'

def ClearCache(key):
    if isinstance(key, list):
        key = []
    elif isinstance(key, dict):
        key = []
    return key

def ClearDictNullValue(data):
    if not isinstance(data, dict):
        return False
    for key, value in data.items():
        if not value:
            data.pop(key)
    return data

def DictValueBooleanToStr(data, strvalue):
    str_value_dict = {}
    if not isinstance(data, dict):
        return False
    for key ,value in data.items():
        value = (strvalue, value)
        str_value_dict[key] = value
    return str_value_dict

def NoDuplicateList(data):
    o_list = data
    n_list = []
    for each in o_list:
        if each not in n_list:
            n_list.append(each)
    return n_list

def UpdateDicData(data, addvalue):
    for key, value in data.items():
        data[key] = [addvalue, value]
    return data


def GetDate():
    # '2016-11-11-162455'
    return datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

