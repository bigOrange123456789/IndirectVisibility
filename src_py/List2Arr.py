from Check import Check
from lib.Tool import Tool
class List2Arr:
    def __init__(self,opt,ls1,nameList):
        list={}
        for i in range(len(ls1)):
            list[nameList[i]]=ls1[i]
        self.opt=opt
        config2=Tool.loadJson(self.opt["out.config2"]+".json")
        list_arr,list_index=self.process(config2,list)
        Tool.saveJson(opt["out7_d_arr"],list_arr)
        Tool.saveJson(opt["out7_d_index"],list_index)
        self.result=[list_arr,list_index]

    def process(self,config,list):
        list_arr=[]
        list_index={}
        step=config["step"]
        for i1 in range(step[0]+1):
            list_arr.append([])
            for i2 in range(step[1]+1):
                list_arr[i1].append([])
                for i3 in range(step[2]+1):
                    name=Check.getName(config,i1,i2,i3)
                    data=list[name]
                    index=i1*(step[1]+1)*(step[2]+1)+i2*(step[2]+1)+i3
                    list_arr[i1][i2].append(data)
                    if len(data)>0:list_index[index]=data
        return [list_arr,list_index]        


if __name__ == "__main__":#用于测试
    print()