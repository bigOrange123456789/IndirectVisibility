import tabnanny
import numpy as np
class NoiseReduction:
  def __init__(self,opt,data2):
    import time as t
    t0=t.time()
    e=self.eigenMat(data2)
    print("step3.执行时间："+str(((t.time()-t0)/60))+" min")
    self.result=[e,t.time()-t0]
  @staticmethod
  def eigenMat(data2):#获得特征矩阵
    # T.w(e,self.opt["out3"])
    return data2#降噪算法现在有问题
    #data2=np.array(data2).T
    U,Sigma,VT=np.linalg.svd(data2)
    Sigma_sum=np.sum(Sigma)

    for i in range(len(Sigma)):
        if np.sum(Sigma[0:i+1])>=1.*Sigma_sum:
            break
    dim=i+1

    s=np.mat(np.eye(dim)*Sigma[:dim])
    sI=np.linalg.inv(s)

    temp=np.matmul(U[:,0:dim],sI)
    temp=np.matmul(np.array(data2).T,temp)
    temp=temp.T

    return temp.tolist()
    #return data2#每一列是一个特征
if __name__ == "__main__":#用于测试
    print()