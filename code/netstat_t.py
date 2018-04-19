#!/usr/bin/python3
#18020512#
import pwd
import os
import re
import glob
import time

PROC_TCP = "/proc/net/tcp"
STATE = {
        '01':'ESTABLISHED',
        '02':'SYN_SENT',
        '03':'SYN_RECV',
        '04':'FIN_WAIT1',
        '05':'FIN_WAIT2',
        '06':'TIME_WAIT',
        '07':'CLOSE',
        '08':'CLOSE_WAIT',
        '09':'LAST_ACK',
        '0A':'LISTEN',
        '0B':'CLOSING'
        }

def _load():
    ''' Read the table of tcp connections & remove header  '''
    with open(PROC_TCP,'r') as f:
        content = f.readlines()
        content.pop(0)
    return content

def _hex2dec(s):
    return str(int(s,16))

def _hex2dec_i(s):
    return int(s,16)

def _ip(s):
    ip = [(_hex2dec(s[6:8])),(_hex2dec(s[4:6])),(_hex2dec(s[2:4])),(_hex2dec(s[0:2]))]
    return '.'.join(ip)

def _remove_empty(array):
    return [x for x in array if x !='']

def _convert_ip_port(array):
    host,port = array.split(':')
    return _ip(host),_hex2dec(port),_hex2dec_i(port)

def writefile_buf(buf):
    with open('/cw/o/s_stauts','a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
        f.write(buf+'\n\n')

def writefile(buf,port):
    with open('/cw/o/s_stauts','a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime()))
        f.write('Port:%s '%port+buf+'\n\n')    

def netstat():
    '''
    Function to return a list with status of tcp connections at linux systems
    To get pid of all network process running on system, you must run this script
    as superuser
    '''

    content=_load()
    result = []
    for line in content:
        line_array = _remove_empty(line.split(' '))     # Split lines and remove empty spaces.
        l_host,l_port,li_port = _convert_ip_port(line_array[1]) # Convert ipaddress and port from hex to decimal.
        r_host,r_port,ri_port = _convert_ip_port(line_array[2]) 
        tcp_id = line_array[0]
        state = STATE[line_array[3]]
        #uid = pwd.getpwuid(int(line_array[7]))[0]       # Get user from UID.
        inode = line_array[9]                           # Need the inode to get process pid.
        pid = _get_pid_of_inode(inode)                  # Get pid prom inode.
        '''try:                                            # try read the process name.
            exe = os.readlink('/proc/'+pid+'/exe')
        except:
            exe = None
'''
        if (li_port < 3000 or li_port >= 4000) and (ri_port < 3000 or ri_port >= 4000):
            continue
        if (line_array[3] == '01' or line_array[3] == '0A') and (pid != None):
        	continue

        writefile(state,li_port)
        nline = [tcp_id,  l_host+':'+l_port, r_host+':'+r_port, state, pid]
        result.append(nline)
    return result

def _get_pid_of_inode(inode):
    '''
    To retrieve the process pid, check every running process and look for one using
    the given inode.
    '''
    for item in glob.glob('/proc/[0-9]*/fd/[0-9]*'):
        try:
            if re.search(inode,os.readlink(item)):
                return item.split('/')[2]
        except:
            pass
    return None

if __name__ == '__main__':
    Loop = 0
    writefile_buf("watching socket")
    while True:
        Flag = False
        for conn in netstat():
            print(conn)
            Flag = True
        time.sleep(15)

        if Flag == True:
            Loop += 1

        if Loop >= 4:
            print('reboot now')
            os.system('reboot')
        time.sleep(1)
