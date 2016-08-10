#! /usr/bin/env python
# coding:utf-8
#********************************************************************
#
# version: 1.0
#
# Description: execute shell cmd in remote linux servers in multi-process
#				
# Input File: ip.txt in the current directory
#             ip1,user,pwd_for_user,pwd_for_root,shell_cmd    
#              seperated by comma
#
# Author: Laury Miao   miupeng@cpic.com.cn
#
# Date: 1 Jul 2016
# 
#********************************************************************

import paramiko
import os
import re
import time
import sys

paramiko.util.log_to_file('paramiko.log')


def ssh_su(ip, user, password, su_passwd, cmd):
    print '-' * 21
    print '-' * 4 + ip + '-' * 4
    print '-' * 21
    t = paramiko.SSHClient()
    t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    t.connect(ip, 22, user, password, timeout=30)
    ssh = t.invoke_shell()
    time.sleep(0.1)
    resp = ssh.recv(9999)
    # print resp

    ssh.send("su - root\n")
    buff = ''

    while not buff.endswith('Password: ') and not resp == '':
        try:
            resp = ssh.recv(9999)
        except Exception as e:
            print 'Error info:%s connection time' % (str(e))
            t.close()
            sys.exit()
        buff += resp
        # print resp

    ssh.send(su_passwd + '\n')
    buff1 = ''
    while True:
        try:
            resp = ssh.recv(500)
        except Exception as e:
            print 'Error info:%s connection time' % (str(e))
            t.close()
            sys.exit()
        buff1 += resp
        # print resp

        if buff1.endswith(('#', '# ')) or resp == '':
            print "su: RIGHT!"
            break
        ### some bugs here (won't ending )with wrong su_passwd 
        else:
            print 'su: WRONG'
            break

    ssh.send(cmd + '\n')
    buff = ""
    bufflog = ''
    while not buff.endswith("# ") and not buff.endswith("#"):
        resp = ssh.recv(100)
        buff += resp
        bufflog += resp.strip('\r\n')
        # print bufflog
        print resp

    t.close()
    print '=' * 60
    return 0

def readfile(filename):
    try:
        fileHandle = open(filename, 'r')
        iplines = fileHandle.read().splitlines()
        fileHandle.close()
        # print iplines
        return iplines
    except IOError as error:
        print 'Read File Error: %s' % error
        sys.exit()

def sftp_get(ip, user, password, remotefile, localfile):
    print '-' * 21
    print '-' * 4 + ip + '-' * 4
    print '-' * 21
    try:
        t = paramiko.Transport((ip, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotefile, localfile)
    except Exception, e:
        print "Failuer:%s <--- %s(%s)" % (localfile, remotefile, e)
        return False
    else:
        t.close()
        print "+Get File is OK"
        return True

def sftp_put(ip, user, password, localfile, remotefile):
    print '-' * 21
    print '-' * 4 + ip + '-' * 4
    print '-' * 21
    try:
        t = paramiko.Transport(sock=(ip, 22))
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(localfile, remotefile)
    except Exception, e:
        print "Failuer:%s ---> %s(%s)" % (remotefile, localfile, e)
        return False
    else:
        t.close()
        print "+Put File is OK"
        return True



import multiprocessing

if __name__ == '__main__':
    print '=' * 20
    pool = multiprocessing.Pool(processes=4)

    for line in readfile('ip.txt'):
        # print line
        ip = line.split(',')[0]
        port = 22
        user = line.split(',')[1]
        passwd = line.split(',')[2]
        su_passwd = line.split(',')[3]
        cmd = line.split(',')[4]
        #pool.apply_async(sftp_put(ip, user, passwd, 'D:/py/nas.sh', '/tmp/nas.sh'))
        pool.apply_async(ssh_su, (ip, user, passwd, su_passwd, cmd))
    pool.close()
    pool.join()
