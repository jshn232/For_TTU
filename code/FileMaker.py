#! /usr/bin/python3
import os
import shutil
import struct

def crc16(f):
	a = 0xFFFF
	b = 0xA001
	for byte in f:
		a ^= byte
		for i in range(8):
			last = a % 2
			a >>= 1
			if last == 1:
				a ^= b
	return a

print("###Make Download File by Python###")

FileName = "Z161_3205_2018012612_zj.sv 2"
ShellFileName = "udisk-down_zip.sh"
NewFileName = "Z161_3205_2018012612_zj_d.sv"


print("File is \"%s\" "%FileName)
if os.path.isfile("./%s" %FileName) == False:
	print("File \"%s\" is not exists!" %FileName)
	print("Exit now")
	exit()
if os.path.isfile("./%s" %ShellFileName) == False:
	print("File \"%s\" is not exists!" %ShellFileName)
	print("Exit now")
	exit()

FileSize = os.path.getsize("./%s" %FileName)
print("File Size is %d Byte" %FileSize)

Mod = 16 - (FileSize % 16)

print("File Making....")
shutil.copyfile(FileName,NewFileName)
with open("./%s" %NewFileName,'ab') as f:
	for i in range(Mod):
		f.write(struct.pack('b',0x00))   #补齐

with open("./%s" %ShellFileName,'r') as sf:
	print("Shell Loading...")
	for line in sf:		
		line = line.strip('\n')		
		with open("./%s" %NewFileName,'a') as f:
			f.write(line)	
		with open("./%s" %NewFileName,'ab') as f:	
			f.write(struct.pack('i',0x00))   #四个字节的0x00	

with open("./%s" %NewFileName,'ab') as f:
	f.write(struct.pack('i',(FileSize+Mod)))  #脚本首地址

print("CRC Calculating...")
NewFileSize = os.path.getsize("./%s" %NewFileName)
with open("./%s" %NewFileName,'rb') as f:
	crc = crc16(f.read())
	print("CRC is %02X"%crc)


print("Factory Info Loading...")
with open("./%s" %NewFileName,'a') as f:
	f.write("creaway")                        #creaway

with open("./%s" %NewFileName,'ab') as f:
	for i in range(13):
		f.write(struct.pack('b',0x00))

	f.write(struct.pack('b',0x05))
	f.write(struct.pack('b',0x32))
	f.write(struct.pack('i',NewFileSize))
	f.write(struct.pack('h',crc))
	for i in range(36):
		f.write(struct.pack('b',0x00))

NewFileSize = os.path.getsize("./%s" %NewFileName)
print("New File Size is %d Byte" %NewFileSize)

print("File Make succeed!")
