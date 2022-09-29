import numpy as np
import json
np.set_printoptions(precision=2)
class Tool:
   def __init__(self):
    print()
   def sim1(self,inA,inB):
    inA=np.array(inA).T
    inB=np.array(inB).T
    num=float(inA.dot(inB))
    denom=np.linalg.norm(inA)*np.linalg.norm(inB)
    if not denom==0:
        return 0.5+0.5*(num/denom)
    else:
        return 0.5
   def sim2(self,inA,inB):
    a=np.array(inA)
    b=np.array(inB)
    denom=np.linalg.norm(a-b)
   @staticmethod
   def clone(x):
       result=[]
       for i in range(len(x)):
           result.append([])
           for j in range(len(x[i])):
               result[i].append(x[i][j])
       return result
   @staticmethod
   def show(data):
    if len(data)>0 and len(data)<100 and isinstance(data[0],list):
        l=len(data[0])
        for i in data:
            if not len(i)==l:
                l=-1
                break
        if l==-1:#各行长度不同
            print(data)
        else:
            print(np.array(data))
    else:
        print(np.array(data))
   
   @staticmethod
   def sort(obj):#由大到小排序
    for i1 in range(len(obj)):
        print(str(round(1000*i1/len(obj))/10)+'%',end="\r")
        i1=len(obj)-i1-1
        max=i1
        for i2 in range(i1):
            if obj[i2]["n"]<obj[max]["n"]:
                max=i2
        temp=obj[max]
        obj[max]=obj[i1]
        obj[i1]=temp
    return obj#data=[{n:1},{n:2}]
   @staticmethod
   def r(name):
    result=[]
    f = open(name+".txt")             # 返回一个文件对象
    line = f.readline()             # 调用文件的 readline()方法
    while line:
        result.append([])
        n=len(result)-1
        arr=line.split(",")
        for i in range(len(arr)):
            result[n].append(float(arr[i]))
        line = f.readline()
    f.close()
    return result
   @staticmethod
   def r_txt(name):
    result=[]
    f = open(name+".txt")             # 返回一个文件对象
    line = f.readline()             # 调用文件的 readline()方法
    while line:
        result.append(line.split("\n")[0])
        line = f.readline()
    f.close()
    return result
   @staticmethod
   def r_json(name):
    if len(name.split(".json"))==1:
        name=name+".json"
    f = open(name, encoding='gb18030', errors='ignore')
    return json.load(f)
   @staticmethod
   def r2(name):
    f = open(name+".json")             # 返回一个文件对象
    import json
    j=json.load(f)
    data=[]
    tagList=[]
    for i in j:
        tagList.append(i)
        data.append(j[i])
    return data,tagList
   @staticmethod
   def w(data,name):
    if name=="":
        return
    print("输出路径：",name)
    #Tool.show(data)
    with open(name+'.txt', 'w') as f:
        for i in range(len(data)):
            if isinstance(data[i],str):
                f.write(data[i])
            else:
                for j in range(len(data[i])):
                    f.write(str(data[i][j]))
                    if j<len(data[i])-1:
                        f.write(",")
            if i<len(data)-1:
                f.write("\n")
            print("save:"+str(round(100*(i+1)/len(data),2))+"%","\t",end="\r")
        print()
   @staticmethod
   def w2(data,name,tagList):
    if name=="":
        return
    print("输出路径：",name)
    #Tool.show(data)
    with open(name+'.json', 'w') as f:
        f.write("{\n")
        for i in range(len(data)):
            f.write('"'+tagList[i]+'":')
            if isinstance(data[i],list):
                f.write('[')
                for j in range(len(data[i])):
                    f.write(str(data[i][j]))
                    if j<len(data[i])-1:
                        f.write(",")
                f.write("]")
            elif isinstance(data[i],str):
                f.write('"'+str(data[i])+'"')
            else:
                f.write(str(data[i]))
            if i<len(data)-1:
                f.write(",\n")
            print("save:"+str(round(100*(i+1)/len(data),2))+"%","\t",end="\r")
        f.write("\n}")
        print()
   @staticmethod
   def loadJson(path):
       import json
       return json.load(open(path))
#    @staticmethod
#    def saveJson(path,data):
#         if path=="":
#             return 
#         import json
#         with open(path, 'w') as write_f:
#             write_f.write(json.dumps(data, indent=4, ensure_ascii=False))
   @staticmethod
   def saveJson(path,data):
        if path=="" or path==".json":
            return
        json.dump(data,open(path,"w"))
