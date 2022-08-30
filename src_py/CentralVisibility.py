from lib.Tool import Tool
import math
import numpy as np
class CentralVisibility:
    def __init__(self,opt,nameList0,d0_):
        self.opt=opt
        if self.opt["CentralVisibility"]:
            config=Tool.loadJson(self.opt["in"]+"/config.json")
            config2=self.getConfig2(config)
            Tool.saveJson(self.opt["out.config2"]+".json",config2)
            data={}
            for i in range(len(nameList0)):
                data[nameList0[i]]=d0_[i]
            data2=self.getData2(config,config2,data)
            nameList_new=[]
            d0_new=[]
            for i in data2:
                nameList_new.append(i)
                d0_new.append(data2[i])
        else:
            nameList_new=nameList0
            d0_new=d0_
        self.result=[nameList_new,d0_new]
    def getConfig2(self,config):
        max=config["max"]
        min=config["min"]
        step=config["step"]
        step_l=[
            (max[0]-min[0])/step[0],
            (max[1]-min[1])/step[1],
            (max[2]-min[2])/step[2]
        ]
        max2=[
            max[0]-step_l[0]/2,
            max[1]-step_l[1]/2,
            max[2]-step_l[2]/2
        ]
        min2=[
            min[0]+step_l[0]/2,
            min[1]+step_l[1]/2,
            min[2]+step_l[2]/2
        ]
        step2=[
            step[0]-1,
            step[1]-1,
            step[2]-1,
        ]
        return {
            "max":max2,
            "min":min2,
            "step":step2
        }

    def getName(self,config,i1,i2,i3):
        min=config["min"]
        step=config["step"]
        max=config["max"]
        if step[0]==0:
            x0=min[0]
        else:
            x0=min[0]+(max[0]-min[0])*i1/step[0]
        if step[1]==0:
            y0=min[1]
        else:
            y0=min[1]+(max[1]-min[1])*i2/step[1]
        if step[2]==0:
            z0=min[2]
        else:
            z0=min[2]+(max[2]-min[2])*i3/step[2]
        if math.floor(x0)==x0:x0=int(x0)
        if math.floor(y0)==y0:y0=int(y0)
        if math.floor(z0)==z0:z0=int(z0)
        return str(x0)+","+str(y0)+","+str(z0)
    def getNames_round(self,config1,i1,i2,i3):
        return [
            self.getName(config1,i1,i2,i3),
            self.getName(config1,i1,i2,i3+1),
            self.getName(config1,i1,i2+1,i3),
            self.getName(config1,i1,i2+1,i3+1),
            self.getName(config1,i1+1,i2,i3),
            self.getName(config1,i1+1,i2,i3+1),
            self.getName(config1,i1+1,i2+1,i3),
            self.getName(config1,i1+1,i2+1,i3+1),
        ]
    def getData2(self,config1,config2,data):
        step=config2["step"]
        data2={}
        for i1 in range(step[0]+1):
            for i2 in range(step[1]+1):
                print(str(i1+1)+"/"+str(step[0]+1)+"   ","\t",str(i2+1)+"/"+str(step[0]+1)+"   ",end="\r")
                for i3 in range(step[2]+1):
                    names=self.getNames_round(config1,i1,i2,i3)
                    name2=self.getName(config2,i1,i2,i3)
                    data2[name2]=[]
                    for name in names:
                        data2[name2].append(data[name])
                    data2[name2]=np.array(data2[name2]).sum(axis=0).tolist()
        return data2
