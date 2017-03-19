#!/usr/bin/python
# -*-coding:utf-8-*-
import urllib2
import socket
import struct
import time
import logging
import telnetlib
import thread
import sys


sms_server = '0.0.0.0'
sms_port = 456

file_log_name = sys.argv[0].split('.')[0] + '.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s  %(filename)s[line:%(lineno)d]:%(levelname)s:%(message)s',
                    datefmt='%Y-%b-%d,%H:%M:%S',
                    filename=file_log_name,
                    filemode='w')


def send_sms_text(text):
    global sms_port, sms_server, phone_list

    address = (sms_server, sms_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    ntext = str(chr(len(text)) + text)
    msglen = 4+12+len(ntext)
    strc_format = str('<cHHI12s'+str(len(ntext))+'s')

    for phone in phone_list:
        nphone = str(chr(len(phone)) + phone)
        msgcontant = struct.pack(strc_format, '0', msglen, 4, 0, nphone, ntext)
        s.send(msgcontant)
    s.close()


def Telnet_ssh(local_IP):
    try:
        tc = telnetlib.Telnet(local_IP, 22, 5)
        uw = tc.read_until("\r\n")
        if 'OpenSSH' in uw:
            return True
        tc.close()
    except:
        return False


def run_monitor_voice(local_IP, ip_describe):
    error_num = 0
    huifu_status = False
    normal_str = 'voice 服务器 ' + local_IP + ' ' + ip_describe + ' 正常;'
    alert_str = 'voice 服务器 ' + local_IP + ' ' + ip_describe + ' 出现不可用;'
    continue_alert_str = 'voice 服务器 ' + local_IP + ' ' + ip_describe + ' 持续出现错误,不发短信;'
    restore_str = 'voice 服务器 ' + local_IP + ' ' + ip_describe + ' 已恢复;'

    while True:
        if Telnet_ssh(local_IP) and huifu_status is False:
            error_num = 0
        elif Telnet_ssh(local_IP) and huifu_status is True:
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
            print 'voice 服务器 %s %s 第 %s 次错误;' % (local_IP, ip_describe, error_num)
            logging.debug('voice 服务器 %s %s 第 %s 次错误;' % (local_IP, ip_describe, error_num))
        elif error_num == 4:
            print alert_str
            send_sms_text(alert_str)
            logging.debug(alert_str)
            huifu_status = True
        else:
            print continue_alert_str
            logging.debug(continue_alert_str)

        time.sleep(60)


if __name__ == "__main__":
    thread.start_new_thread(run_monitor_voice, ('8.88.8', 'vip-jiuyinzhenjing'))
    thread.start_new_thread(run_monitor_voice, ('0.0.0.0', 'vip-boke'))



    while True:
        time.sleep(10)