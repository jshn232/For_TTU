import numpy as np
import pylab as pl
import time
x1=[]
x2=[]
y1=[]
y2=[]
with open('./record1','r') as f:
	for s in f.readlines():
		strlist = s.split(',')
		if len(strlist) == 3:
			rTime = time.strptime(strlist[0],'%Y-%m-%d %H:%M:%S')
			strTime = str.format("%02d:%02d"%(rTime.tm_hour,rTime.tm_min))
			x1.append(strTime)
			x2.append(strTime)
			y1.append(float(strlist[1]))
			y2.append(float(strlist[2]))


pl1 = pl.plot(x1, y1,'r')# use pylab to plot x and y

pl2 = pl.plot(x2, y2,'b')# use pylab to plot x and y

pl.legend([pl1, pl2], ('cpu', 'env'))
pl.show()# show the plot on the screen
