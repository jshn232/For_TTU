#MakeDeployFile
import re
import os
import os.path

TarList = []
#列出文件夹内所包含的容器列表
for lists in os.listdir("./"):
    if lists[-4:] == ".tar":
        if lists.find("msptl") != -1:
            Msptl = lists[:-4]
        if lists.find("sample") != -1:
            Sample = lists[:-4]
        if lists.find("com_32xx_sk") != -1:
            Com_sk = lists[:-4]
        if lists.find("com_32xx_sl") != -1:
            Com_sl = lists[:-4]
        if lists.find("security") != -1:
            Security = lists[:-4]
        if lists.find("umeter") != -1:
            Umeter = lists[:-4]
        if lists.find("chp") != -1:
            Chp = lists[:-4]
    if lists[-4:] == ".bin":
        if lists.find("gprsdial") != -1:
            Gprsdial = lists[:-4]
        if lists.find("watch") != -1:
            Watchip = lists[:-4]



#逐一查找需要部署的容器类型及所在原始文件的位置
#找到容器列表的名称
#替换
with open("deploy_sk.demo", "r+") as fin:
    with open("deploy_sk.sh", "w+") as fout:
        for line in fin:
            line = line.replace('*msptl*', Msptl)
            line = line.replace('*sample*', Sample)
            line = line.replace('*com_32xx_sk*', Com_sk)
            line = line.replace('*com_32xx_sl*', Com_sl)
            line = line.replace('*security*', Security)
            line = line.replace('*umeter*', Umeter)
            line = line.replace('*chp*', Chp)
            line = line.replace('*gprsdial*', Gprsdial)
            line = line.replace('*watchip*', Watchip)
            fout.write(line)

with open("deploy_sl.demo", "r+") as fin:
    with open("deploy_sl.sh", "w+") as fout:
        for line in fin:
            line = line.replace('*msptl*', Msptl)
            line = line.replace('*sample*', Sample)
            line = line.replace('*com_32xx_sk*', Com_sk)
            line = line.replace('*com_32xx_sl*', Com_sl)
            line = line.replace('*security*', Security)
            line = line.replace('*umeter*', Umeter)
            line = line.replace('*chp*', Chp)
            line = line.replace('*gprsdial*', Gprsdial)
            line = line.replace('*watchip*', Watchip)
            fout.write(line)
