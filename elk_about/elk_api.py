#!/usr/bin/env python
#coding=utf8
import requests
import elk_parms
import datetime
import json
import time
import socket
import struct
import logging
import sys


def search(request_uri, json_data):
    """Simple Elasticsearch Query"""
    try:
        query = json.dumps(json_data)
        response = requests.get(request_uri, data=query)
        if response.status_code is not 200:
            return False
        results = json.loads(response.text)
        return results
    except Exception, e:
        print sys._getframe().f_lineno, e
        return False


def time_convert(minutes):
    if not isinstance(minutes, int):
        print 'Error: ' + str(minutes) + ' is not int'
        return (False, None)
    file_time = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    unix_now = int(time.mktime(datetime.datetime.now().timetuple())) * 1000
    Abst_tim = unix_now - minutes * 60 * 1000
    return_data = {'file_time': file_time, 'gte': Abst_tim, 'lte': unix_now}
    return (True, return_data)


def C_live_new_nginx_metric_upstream_response_time(minutes):
    return_dir = {}
    about_time = time_convert(minutes)
    if about_time[0] is False:
        return False
    request_uri = 'http://0.0.0.0:9200/logstash-live-online-%s/_search' % about_time[1]['file_time']
    json_data = elk_parms.C_live_new_nginx_metric_upstream_response_time(about_time[1]['gte'], about_time[1]['lte'])
    res_data = search(request_uri, json_data)
    if res_data is False:
        return False
    return_dir['total_count'] = res_data['hits']['total']
    return_dir['max_re_time'] = res_data['aggregations']['2']['value']
    return_dir['avg_re_time'] = res_data['aggregations']['3']['value']
    return_dir['min_re_time'] = res_data['aggregations']['4']['value']
    rank_value = res_data['aggregations']['5']['values']
    return_dir['rank_zero_point_two'] = rank_value['0.2']
    return_dir['rank_zero_point_eight'] = rank_value['0.8']
    return_dir['rank_one_point_two'] = rank_value['1.2']
    return_dir['rank_two_point_two'] = rank_value['2.2']
    # print return_dir
    return return_dir


def handle_func(minutes, triger_total_count, triger_rank_two_point_two, triger_max_re_time):
    response_data =  C_live_new_nginx_metric_upstream_response_time(minutes)
    if response_data is False:
        print 'elk 请求数据失败;'
        logging.debug('elk 请求数据失败;')
        return (True, None)
    print 'total_count: %s' % response_data['total_count']
    logging.debug('total_count: %s' % response_data['total_count'])
    print 'rank_two_point_two: %s' % response_data['rank_two_point_two'] + '%'
    logging.debug('rank_two_point_two: %s' % response_data['rank_two_point_two'] + '%')
    print 'max_re_time: %ss' % response_data['max_re_time']
    logging.debug('max_re_time: %ss' % response_data['max_re_time'])

    if response_data['total_count'] > triger_total_count and response_data['rank_two_point_two'] < triger_rank_two_point_two and response_data['max_re_time'] > triger_max_re_time:
        return (False, 'total_count,rank_two_point_two,max_re_time 均')

    if response_data['total_count'] > triger_total_count and response_data['rank_two_point_two'] < triger_rank_two_point_two:
        return (False, 'total_count,rank_two_point_two 均')

    if response_data['total_count'] > triger_total_count and response_data['max_re_time'] > triger_max_re_time:
        return (False,'total_count,max_re_time 均')

    if response_data['rank_two_point_two'] < triger_rank_two_point_two and response_data['max_re_time'] > triger_max_re_time:
        return (False, 'rank_two_point_two,max_re_time 均')

    if response_data['total_count'] > triger_total_count:
        return (False, 'total_count')

    if response_data['rank_two_point_two'] < triger_rank_two_point_two:
        return (False, 'rank_two_point_two')

    if response_data['max_re_time'] > triger_max_re_time:
        return (False, 'max_re_time')

    return (True, None)



sms_server = '0.0.0.0'
sms_port = 66666

file_log_name = sys.argv[0].split('.')[0] + '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(filename)s[line:%(lineno)d]:%(levelname)s:%(message)s',
                    datefmt='%Y-%b-%d,%H:%M:%S',
                    filename=file_log_name,
                    filemode='w')
error_num = 0
huifu_status = False
normal_str = 'c 数值监控正常;'
alert_str = 'c 数值监控 %s 达到阀值;'
continue_alert_str = 'c 数值监控持续报警;'
restore_str = 'c 数值监控恢复正常;'
minutes = 1
triger_total_count = 50000
triger_rank_two_point_two = 80
triger_max_re_time = 30

while True:
    handle_run = handle_func(minutes, triger_total_count, triger_rank_two_point_two, triger_max_re_time)
    if handle_run[0] and huifu_status is False:
        error_num = 0
    elif handle_run[0] and huifu_status is True:
        error_num = 0
        huifu_status = False
        logging.debug(restore_str)
        send_sms_text(restore_str)
        print restore_str
    else:
        error_num += 1

    if error_num == 0:
        print normal_str
        logging.debug(normal_str)
    elif 0 < error_num < 4:
        print '第 %s 次错误;' % error_num
        logging.debug('第 %s 次错误;' % error_num)
    elif error_num == 4:
        print alert_str % handle_run[1]
        send_sms_text(alert_str % handle_run[1])
        logging.debug(alert_str % handle_run[1])
        huifu_status = True
    else:
        print continue_alert_str
        logging.debug(continue_alert_str)

    time.sleep(60)



