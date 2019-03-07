import os
import time
import subprocess

t_old = 0

def _getDockerStats(cont):
    stats = subprocess.getoutput("docker stats msptl --no-stream --format "+ "{{.MemUsage}}")
    return stats

def test(cont):
    with open("/cw/o/Stats_"+cont, "a") as f:
        f.write(str(time.strftime("%Y-%m-%d %H:%M:%S,")))
        f.write(str(_getDockerStats(cont))+"\n")

def monitor(cont,mins):
    global t_old
    day = 0
    timelocal = time.localtime(time.time())
    t_min = timelocal.tm_min
    if (t_min % mins == 0) and (t_min != t_old):  # 5分钟一个周期
        if (day != timelocal.tm_yday):
            day = timelocal.tm_yday
            s_day = str(time.strftime("%Y%m%d"))
        with open("/cw/o/Stats_"+cont+"_"+s_day, "a") as f:
            f.write(str(time.strftime("%Y-%m-%d %H:%M:%S,")))
            f.write(str(_getDockerStats(cont))+"\n")
            t_old = t_min

if __name__ == '__main__':
#    test("msptl")
    while True:
        monitor("msptl",2)
        time.sleep(30)
