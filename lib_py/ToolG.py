from numba import cuda
import numpy as np
GPU_PARAM={
    "max1":800,#THREAD_INDEX_MAX1,
    "max2":600,#THREAD_INDEX_MAX2,
    "max3":500#THREAD_INDEX_MAX3
}
print("GPU_PARAM:",GPU_PARAM)
#0.
@cuda.jit
def addGPU(A,B,C):
    i=cuda.blockIdx.x
    j=cuda.threadIdx.x
    C[i][j]=A[i][j]+B[i][j]
@cuda.jit
def mulGPU(A,B,C,k):
    i=cuda.blockIdx.x
    j=cuda.threadIdx.x
    C[i][j]=0
    for k0 in range(k):
        C[i][j]=C[i][j]+A[i][k0]*B[k0][j]
#1.
#2.去除冗余
@cuda.jit
def getDistGPU(C,S,D,k):
    i=cuda.blockIdx.x
    j=cuda.threadIdx.x
    D[i][j]=0
    for k0 in range(k):
        D[i][j]=D[i][j]+(C[i][k0]-S[j][k0])**2
#6.计算资源加载列表
@cuda.jit
def sortGPU(L,O,j):
    k=cuda.threadIdx.x
    for a in range(j):
        O[k][a]=a
    for a in range(j):
        a=j-1-a#未排序部分的最后一个
        maxIndex=a
        for b in range(a):
            if L[k][b]<L[k][maxIndex]:
                maxIndex=b 
        if not maxIndex==a:
            temp=L[k][a]
            L[k][a]=L[k][maxIndex]
            L[k][maxIndex]=temp
            temp=O[k][a]
            O[k][a]=O[k][maxIndex]
            O[k][maxIndex]=temp
        
class ToolG:
   def __init__(self):
    print()
   #0.测试
   @staticmethod
   def add(a,b):
    i1=len(a)
    if i1<1:
        return []
    i2=len(a[0])
    d_A = cuda.to_device(a)
    d_B = cuda.to_device(b)
    d_C = cuda.to_device(np.zeros((i1,i2)))
    addGPU[i1, i2](d_A,d_B,d_C)
    return d_C.copy_to_host()
   @staticmethod
   def mul(a,b):
    i1=len(a)
    if i1<1 or len(b)<1:
        return []
    i2=len(a[0])
    i3=len(b[0])
    d_A = cuda.to_device(a)
    d_B = cuda.to_device(b)
    d_C = cuda.to_device(np.zeros((i1,i3)))
    mulGPU[i1, i3](d_A,d_B,d_C,i2)
    return d_C.copy_to_host()
   #1.
   #2.去除冗余
   @staticmethod
   def getDist0(centroids,dataSet):#用于k-mean: 计算元素到质心的距离平方 #比较大小不需要开根号
    i1=len(centroids)
    i2=len(dataSet)
    k=len(dataSet[0])
    #print({
    #    "centroids":[i1,len(centroids[0])],
    #    "dataSet":[i2,len(dataSet[0])]
    #    })
    #print("dataSet",i2,len(dataSet[0]))

    C = cuda.to_device(centroids)
    S = cuda.to_device(dataSet)
    D = cuda.to_device(np.zeros((i1,i2)))
    getDistGPU[i1, i2](C,S,D,k)
    return D.copy_to_host()
   @staticmethod
   def getDist1(centroids,dataSet):#用于k-mean: 计算元素到质心的距离平方 #比较大小不需要开根号
    #centroids=centroids.tolist()
    #dataSet=dataSet.tolist()#数据过大的化需要分散处理
    #print(dataSet)
    i2=len(dataSet)

    dist=[]
    dataSet_index=0
    part_length=GPU_PARAM["max1"]#THREAD_INDEX_MAX1#500#300#THREAD_INDEX_MAX1
    while dataSet_index<i2:
        dataSet_part=[]
        for i in range(part_length):
            if dataSet_index<i2:
                dataSet_part.append(dataSet[dataSet_index].tolist()[0])#dataSet_part.append(dataSet[dataSet_index])
                dataSet_index=dataSet_index+1
        #print("dataSet_part:\n",np.array(dataSet_part))
        dist_part=ToolG.getDist0(centroids,dataSet_part)
        for i in dist_part.T:
            dist.append(i.tolist())
        print(str(round(100*dataSet_index/i2,2))+"%","\t",str(dataSet_index)+"/"+str(i2),end="\r")
    print("\t\t\t\t\t\t\t",end="\r")
    return np.array(dist).T
   @staticmethod
   def getDist(centroids,dataSet):
    i1=len(centroids)    

    dist=[]
    centroids_index=0
    part_length=GPU_PARAM["max2"]#THREAD_INDEX_MAX2#500#100
    while centroids_index<i1:
        #print(centroids_index,i1)
        centroids_part=[]
        for i in range(part_length):
            if centroids_index<i1:
                centroids_part.append(centroids[centroids_index].tolist()[0])
                centroids_index=centroids_index+1
        dist_part=ToolG.getDist1(centroids_part,dataSet)
        for i in dist_part:
            dist.append(i.tolist())
    return np.array(dist)
   #3.
   #4.
   #5.
   #6.计算资源加载列表
   @staticmethod
   def sort0(lists):
       i=len(lists)
       j=len(lists[0])
       L = cuda.to_device(lists)
       O = cuda.to_device(np.zeros((i,j)))
       sortGPU[1, i](L,O,j)
       return O.copy_to_host()
   @staticmethod
   def sort(lists):
       order=[]
       lists_index=0
       part_length=GPU_PARAM["max3"]#THREAD_INDEX_MAX3
       while lists_index<len(lists):
        lists_part=[]
        for i in range(part_length):
            if lists_index<len(lists):
                lists_part.append(lists[lists_index])
                lists_index=lists_index+1
        order_part=ToolG.sort0(lists_part)
        for i in order_part:
            order.append(i.tolist())
       return order
if __name__ == "__main__":#用于测试
    print()
    A=np.array([
        [1,0,0],
        [0,2,0],
        [0,0,1]
    ])
    B=np.array([
        [1,0,0],
        [0,1,1],
        [0,1,1]
    ])
    d=ToolG.getDist(A,B)
    print(d)
    #0 3 3
    #5 2 2
    #  
    order=ToolG.sort(A)
    print(order)
    #0 1 2
    #1 0 2
    #2 1 0
 