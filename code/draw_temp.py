# -*- coding: UTF-8 -*-
import numpy as np
import pylab as pl
import time
import os
x1=[]
x2=[]
x3=[]
y1=[]
y2=[]
y3=[]
module_path = os.path.dirname(__file__)
filename = module_path + '/record1'
with open(filename,'r') as f:
	for s in f.readlines():
		strlist = s.split(',')
		if len(strlist) == 4:
			rTime = time.strptime(strlist[0],'%Y-%m-%d %H:%M:%S')
			strTime = str.format("%02d:%02d"%(rTime.tm_hour,rTime.tm_min))
			x1.append(strTime)
			x2.append(strTime)
			x3.append(strTime)
			y1.append(float(strlist[1]))
			y2.append(float(strlist[2]))
			y3.append(float(strlist[3]))


pl1, = pl.plot(x1, y1,'r')# use pylab to plot x and y

pl2, = pl.plot(x2, y2,'b')# use pylab to plot x and y

pl3, = pl.plot(x3, y3,'y')

pl.legend([pl1, pl2, pl3], ('cpu_t', 'env_h','env_t'))

pl.show()# show the plot on the screen