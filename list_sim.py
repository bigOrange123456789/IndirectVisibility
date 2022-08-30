import json
import os
import math
import time as t
import numpy as np
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
path0="list/"
print("1.读取config文件")
config=getJson(path0+"config.json")
data=getJson(path0+"all1.json")

print("2.检验数据的完整性")
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
def check(data,config):
    step=config["step"]
    for i1 in range(step[0]+1):
        print(i1,"\t",step[0]+1,end="\r")
        for i2 in range(step[1]+1):
            for i3 in range(step[2]+1):
                viwerPoint=getName(config,i1,i2,i3)
                # print(viwerPoint,viwerPoint in data)
                if viwerPoint in data:
                    print("视点不存在:",viwerPoint)
                    exit(0)
    print("已完成检测   ")
print("1637,-1.5,-2057.5" in data)
print("1637" in data)

check(data,config)
exit(0)
print("3.开始逐个文件进行排序")
def sort_json(json_data):
    keys=[]
    values=[]
    for key,value in json_data.items():
        keys.append(int(key))
        values.append(value)
    index=np.argsort(-np.array(values))
    result=np.array(keys)[index].tolist()
    result_values=np.array(values)[index].tolist()
    return [result,result_values]
def mySort(path0,config):
    step=config["step"]
    result=[]
    for i1 in range(step[0]+1):
        result1=[]
        print(i1,"\t",step[0]+1,end="\r")
        for i2 in range(step[1]+1):
            result2=[]
            for i3 in range(step[2]+1):
                path=path0+getName(config,i1,i2,i3)+".json"
                json_data=getJson(path)
                sort_result=sort_json(json_data)
                result2.append(
                    sort_result[0]
                )
            result1.append(result2)
        result.append(result1)
    return result
result=mySort("huayi/all1/",config)
saveJson("all1.json",result)
result=mySort("huayi/all2/",config)
saveJson("all2.json",result)