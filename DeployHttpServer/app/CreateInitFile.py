# -*- coding: utf-8 -*-
import os


tomcat_init_data = '''#!/bin/bash

. /etc/profile

stop() {
        A=`ps -ef | grep -i "%s" | grep -v grep | awk '{print $2}'`
        kill -9 $A
}

start() {
        %s/bin/startup.sh
}

case "$1" in
    restart)
        stop
        ;;
    stop)
        stop
        ;;
esac
'''

im_init_data = '''#!/bin/bash

. /etc/profile

stop() {
        A=`ps -ef | grep -i "%s" | grep -v grep |grep -vi CheckScript |awk '{print $2}'`
        kill -9 $A
}

case "$1" in
    restart)
        stop
        ;;
    stop)
        stop
        ;;
esac
'''



def FindInitFileName(data):
    if '.' in data:
        data = data.split('.')
        data = data[0]
    return data

def FindTomcatInitKeyWord(data):
    data = data.split('/')
    index = data.index('webapps')
    data = data[:index]
    data = "/".join(data)
    # print data
    return data

def CreateTomcatInitFile(filedata, filename, filepath, createfilepath,ifchmod=True):
    filename = 'r-' + FindInitFileName(filename)
    file = os.path.join(createfilepath, filename)
    fp = open(file, 'w')
    key_word = FindTomcatInitKeyWord(filepath)
    filedata = filedata % (key_word, key_word)
    fp.write(filedata)
    fp.close()
    if ifchmod:
        os.system('chmod +x %s' % file)
    return filename

def FindImInitKeyWord(data):
    return data

def CreateImInitFile(filedata, filename, filepath, createfilepath, ifchmod=True):
    filename = 'r-' + FindInitFileName(filename)
    file = os.path.join(createfilepath, filename)
    fp = open(file, 'w')
    key_word = FindImInitKeyWord(filepath)
    filedata = filedata % key_word
    fp.write(filedata)
    fp.close()
    if ifchmod:
        os.system('chmod +x %s' % file)
    return filename

# filename = 'vshow-api.war'
# CreateTomcatInitFile(filedata=tomcat_init_data, filename=filename,
#                      filepath= '/data/apache-tomcat-7.0.54-api/webapps/vshow-api.war',
#                      createfilepath = os.path.join('./initfiles', filename))
# filename = 'VShowIMServer'
# CreateImInitFile(filedata=im_init_data, filename=filename, filepath= '/data/VShowIMServer-1/bin/VShowIMServer')



