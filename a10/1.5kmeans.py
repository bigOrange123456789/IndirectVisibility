def loadJson(path):
   import json
   return json.load(open(path))
import sys
if len(sys.argv)<2:
    print("ERR:请指定config.json的路径")
    exit(0)
path=sys.argv[1]
config=loadJson(path)
path_pre=config["in_temp"]
path_out_data2=config["out_data2"]
#################################################
path1=""
path2=""
# data=loadJson("1747,-1,-1537.json")
clusterAssment=loadJson(config["in_clusterAssment"])
if False:
    clusterAssment=[0,0,1,1]
    data={
    "1":{
        "0":10,
        "1":1,
        "2":2,
        "3":3
    },
    "2":{
        "0":0,
        "1":1,
        "2":2,
        "3":3
    },
    "3":{
        "0":0,
        "1":1,
        "2":2,
        "3":3
    },
    "4":{
        "0":0,
        "1":1,
        "2":2,
        "3":3
    },
    "5":{
    },
    "6":{
    }
    }

def conversion(data1,clusterAssment):
    data2={}
    for direction in data1:
        d1=data1[direction]
        d2={}
        for i in clusterAssment:
            d2[i]=0
        for id1 in d1:
            visible=d1[id1]
            id2=clusterAssment[int(id1)]
            d2[id2]+=visible
        d2_no0={}
        for id in d2:
            if not d2[id]==0:
                d2_no0[id]=d2[id]
        data2[direction]=d2_no0
    return data2
# data2=conversion(data,clusterAssment)
# print(data2)

######################################

# path_pre="1.move_all"
# path_pre="../4.SamplingOfVisibility/sampling_huayi_113"
import json
import os
import math
import time as t
t00=t.time()
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path) 

jsonPathErr=[]
def getJson(path):
    try:
        return json.load(
            open(path,"r")
        )
    except Exception as e:
        print("无法解析的json文件:",path,e)
        jsonPathErr.append(path)#exit(0)
def saveJson(path,data):
    json.dump(
        data,
        open(path,"w")
    )
def isNull(path):
    if os.path.getsize(path)==0:
        jsonPathErr.append(path)#exit(0)
config=getJson(path_pre+"/config.json")
# print(config)
t0=t.time()
print(int(t0-t00))
print("1.开始检验数据的完整性")
def getName(config,i1,i2,i3):
    min=config["min"]
    step=config["step"]
    max=config["max"]
    x0=min[0]+(max[0]-min[0])*i1/step[0]
    y0=min[1]+(max[1]-min[1])*i2/step[1]
    z0=min[2]+(max[2]-min[2])*i3/step[2]
    if math.floor(x0)==x0:x0=int(x0)
    if math.floor(y0)==y0:y0=int(y0)
    if math.floor(z0)==z0:z0=int(z0)
    return str(x0)+","+str(y0)+","+str(z0)
def check(config):
    step=config["step"]
    flag_nopath=False
    for i1 in range(step[0]+1):
        print(i1,"\t",step[0]+1,end="\r")
        for i2 in range(step[1]+1):
            for i3 in range(step[2]+1):
                path=path_pre+"/"+getName(config,i1,i2,i3)+".json"
                file_exists=os.path.exists(path)
                if not file_exists:
                    print("文件不存在:",path)
                    flag_nopath=True
                else:
                    isNull(path)#data[path]=getJson(path)
                    data1=loadJson(path)
                    data2=conversion(data1,clusterAssment)
                    saveJson(path_out_data2+"/"+getName(config,i1,i2,i3)+".json",data2)

    print("已检测完全部构件     ")
    if len(jsonPathErr)==0:
        print("没有空的json文件")
    else:
        print("无法解析的json文件数量为:",len(jsonPathErr))
        saveJson("jsonPathErr.json",jsonPathErr)
        exit(0)
    if not flag_nopath:
        print("没有缺失的文件")
check(config)
t1=t.time()
print(int(t1-t0))
