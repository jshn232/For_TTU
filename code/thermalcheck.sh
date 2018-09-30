#!/bin/bash

while :
do
     sleep 10
     echo $(date) >> logthermalcheck
     echo $(cat /sys/devices/virtual/thermal/thermal_zone0/temp) >> logthermalcheck
done

