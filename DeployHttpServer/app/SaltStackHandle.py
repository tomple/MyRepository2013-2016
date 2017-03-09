# -*- coding: utf-8 -*-
import salt.client
import DataStructureTool
import os

def FileFind(filename):
    local = salt.client.LocalClient()
    filename = 'name='+filename
    result = local.cmd('*', 'file.find', ['/', filename, "print=name,path"])
    return result

def FileDeploy(hostname, s_filepath, d_filepath):
    local = salt.client.LocalClient()
    s_filepath = 'salt://'+s_filepath
    result = local.cmd(hostname, 'cp.get_file', [s_filepath, d_filepath])
    return result

def FileBackup(hostname,s_filepath, d_filepath, if_remove_source=True):
    local = salt.client.LocalClient()
    d_filepath = d_filepath
    b_filepath = os.path.join('/', DataStructureTool.GetDate(), s_filepath)
    result = local.cmd(hostname, 'cp.push', [d_filepath, 'upload_path',
                                             b_filepath, 'remove_source='+str(if_remove_source)])
    return result

def PillarSet():
    local = salt.client.LocalClient()
    local.cmd('*', 'state.sls', ['cesh', '''pillar={"foo":"bar"}'''])

def ChmodFile(hostname, filepath):
    local = salt.client.LocalClient()
    result = local.cmd(hostname, 'cmd.run', ['chmod +x '+filepath])
    # result = local.cmd(hostname, 'file.set_mode', [filepath 0755])

def RestartServer(hostname, servername):
    local = salt.client.LocalClient()
    result = local.cmd(hostname, 'service.restart', [servername])
    # result = local.cmd(hostname, 'cmd.run', ['/etc/init.d/'+servername+' restart'])
    return result


# PillarSet()

#FileFind("testfile")
#a = FileDeploy("ip-10-0-0-237.cn-north-1.compute.internal", "testfile", "/data/testdir/testfile")
#print a
