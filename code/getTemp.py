#! /usr/bin/python3
#20180423
import struct 
import socket
import time
from binascii import hexlify, unhexlify

TERMAL_TEMP = "/sys/devices/virtual/thermal/thermal_zone0/temp"

#插入
def _insert(original, new, pos):
	return original[:pos] + new + original[pos:]

#获取CPU温度
def _getTerTemp():
	with open(TERMAL_TEMP,'r') as f:
		temp = f.read()

	s_Temp = str(temp)
	s_Temp = _insert(s_Temp,'.',2)
	temp = float(s_Temp)
	return temp

#获取环境温度
def _getEnvTemp():
	try:
		address = ('127.0.0.1', 4001)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		msg = "68FFFFFFFF0A0168010C00010000000000000025D528D5DC16"   #通过UDP 上行通讯获取环境温湿度
		msg = unhexlify(msg)
		s.sendto(msg, address)
		s.settimeout(5)
		rev = s.recv(1024)
		rev = str(hexlify(rev))
#		print("rev:%s"%rev)
		index = rev.find('25d5')
		data1 = rev[index+4:index+8]
		data1 = _insert((data1[2:4]+data1[0:2]),'.',3)

		index = rev.find('28d5')
		data2 = rev[index+4:index+8]
		data2 = _insert((data2[2:4]+data2[0:2]),'.',3)

		s.close()
	except socket.timeout:
		print("rev timeout!")
		s.close()
		return False,0,0
	except:
		print("Error")
		s.close()
		return False,0,0

#	print(data1)
#	print(data2)
	if (data1 == "fff.f") or (data2 == "fff.f"):
		return False,0,0
	else:
		try :
			f_data1 = float(data1)
			f_data2 = float(data2)
		except:
			return False,0,0
		return True,f_data1,f_data2

def _udpGetTemp():
	try:
		address = ('127.0.0.1', 4001)
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		msg = "68FFFFFFFF0A0168010C00010000000000000025D528D5DC16"   #通过UDP 上行通讯获取环境温湿度
		msg = unhexlify(msg)
		s.sendto(msg, address)
		s.settimeout(5)
		rev = s.recv(1024)
		rev = str(hexlify(rev))
		print("rev:%s"%rev)
		index = rev.find('25d5')
		data1 = rev[index+4:index+8]
		data1 = _insert((data1[2:4]+data1[0:2]),'.',3)

		index = rev.find('28d5')
		data2 = rev[index+4:index+8]
		data2 = _insert((data2[2:4]+data2[0:2]),'.',3)

		s.close()
	except socket.timeout:
		print("rev timeout!")
		s.close()
	except:
		print("Error")
		s.close()

	print(data1)
	print(data2)


def monitor():
	t_old = 0
	day = 0
	timelocal = time.localtime(time.time())
	t_min = timelocal.tm_min
	if (t_min % 5 == 0) and (t_min != t_old):   #5分钟一个周期
		if (day != timelocal.tm_yday):
			day = timelocal.tm_yday
			s_day = str(time.strftime("%Y%m%d"))
		with open("/cw/o/Temp_"+s_day, "a") as f:
			ret,f_data1,f_data2 = _getEnvTemp()
			if ret:
				f.write(str(time.strftime("%Y-%m-%d %H:%M:%S,")))
				f.write(str(_getTerTemp())+','+str(f_data1)+','+str(f_data2) + "\n")
#				print("record successful!")
				t_old = t_min

if __name__ == '__main__':
	while True:
		monitor()
		time.sleep(30)
	
