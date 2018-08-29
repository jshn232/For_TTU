#! /bin/bash

basepath=$(cd `dirname $0`; pwd)
if [ -f "$basepath/Z161_3205_2018062610_zj_ubuntu.sv" ];then
	rm /app/bin/Z161_3205_2018062610_zj_ubuntu.sv
	cp $basepath/Z161_3205_2018062610_zj_ubuntu.sv /app/bin/Z161_3205_2018062610_zj_ubuntu.sv
	chmod 777 /app/bin/Z161_3205_2018062610_zj_ubuntu.sv
	if [ -f "/app/bin/Z161_3205_2018062610_zj_ubuntu.sv" ];then
		rm /app/main.bin
		ln -s /app/bin/Z161_3205_2018062610_zj_ubuntu.sv /app/main.bin
		reboot
	fi
fi