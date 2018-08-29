#! /usr/bin/python3
#20180828
import os
from xml.dom import minidom
import socket
from binascii import hexlify, unhexlify

#数字转字符串（%03d）
def _dec2Str(dec):
	if dec > 255:
		dec = 0
		print("dec pass 255 (%s)" % dec)
	return "{:0>3}".format(str(dec))

#组帧  13为MP  14-15为DI  20为CS
def _frameMsgReadRamData(DI,MP):
   
    msg_hex = [0x68, 0xFF, 0xFF, 0xFF, 0xFF, 0x81, 0x02, 0x68, 0x0F ,0x09 ,0x00 
    ,0x88 ,0x06 ,0x01 ,0x00 ,0x30 ,0x7F ,0x7F ,0x7F ,0x7F, 0x22, 0x16]

    msg_hex[13] = MP
    msg_hex[14] = DI % 0x0100
    msg_hex[15] = DI / 0x0100

    cs_hex = 0
    for i in range(len(msg_hex)-2):
        cs_hex += (msg_hex[i])
    cs_hex = cs_hex % 0x0100

    msg_hex[20] = cs_hex


    msg_str = ""
    for i in range(len(msg_hex)):
        msg_str += "%02X"%int(msg_hex[i])
    print(msg_str)

    return msg_str

def _sendMsgbyDI(DI, MP, s, address):
    msg = _frameMsgReadRamData(DI, MP)
#    msg = "68FFFFFFFF0A0168010C00010000000000000025D528D5DC16"  # 通过UDP 上行通讯获取环境温湿度
    msg = unhexlify(msg)
    s.sendto(msg, address)
    s.settimeout(5)
    rev = s.recv(1024)
    rev = str(hexlify(rev))
    print(rev)
    return rev

# 生成XML文件方式
def _generateXml(s, address):
    impl = minidom.getDOMImplementation()
    # 创建一个xml dom
    # 三个参数分别对应为 ：namespaceURI, qualifiedName, doctype
    doc = impl.createDocument(None, None, None)
    rootElement = doc.createElement('MPP')

    for i in range(1,80):
        MP = 'M' + _dec2Str(i)
        #创建根元素
        #查询测量点有效性
        rev = _sendMsgbyDI(0x3000, i, s, address)
        data = rev[42:44]
        if data == '01':
            print(MP)
        else:
            continue
        #如果无效则查询下一个测量点
        MXX = doc.createElement(MP)
        P3FFF = doc.createElement('P3FFF')
        P31FF = doc.createElement('P31FF')

        P3100 = doc.createElement('P3100')
        rev = _sendMsgbyDI(0x3100, i, s, address)
        data = rev[42:54]
        value = doc.createTextNode(data)
        P3100.appendChild(value)

        P3101 = doc.createElement('P3101')
        rev = _sendMsgbyDI(0x3101, i, s, address)
        data = rev[42:44]
        value = doc.createTextNode(data)
        P3101.appendChild(value)

        P3105 = doc.createElement('P3105')
        rev = _sendMsgbyDI(0x3105, i, s, address)
        data = rev[42:74]
        value = doc.createTextNode(data)
        P3105.appendChild(value)


        P3FFF.appendChild(P31FF)
        P31FF.appendChild(P3100)
        P31FF.appendChild(P3101)
        P31FF.appendChild(P3105)
        MXX.appendChild(P3FFF)
        rootElement.appendChild(MXX)

    # 将拼接好的根元素追加到dom对象
    doc.appendChild(rootElement)

    # 打开test.xml文件 准备写入
    f = open(os.path.abspath('.')+'/MP.xml', 'w')
    # 写入文件
    doc.writexml(f, addindent='  ', newl='\n')
    # 关闭
    f.close()


if __name__ == '__main__':
#    _frameMsgReadRamData(0x3001,0x02)
    address = ('127.0.0.1', 4001)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _generateXml(s, address)
    s.close()
    
