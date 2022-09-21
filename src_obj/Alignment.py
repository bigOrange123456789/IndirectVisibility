# 无法编译
from Mesh import Mesh
import numpy as np

class Alignment:  # 基于PCA
    def __init__(self, mesh1, mesh2):
        self.method="cpca"
        self.mesh1 = mesh1
        self.mesh2 = mesh2
        self.v1 = np.array(self.mesh1.vertex)
        self.v2 = np.array(self.mesh2.vertex)
        self.mat, self.normal1, self.normal2 = self.compute()
    def compute(self):
        if self.method=="cpca":
            mat1, mean1, normal1 = self.cpca(self.v1, 3,self.mesh1)  # obj0=(obj1-mean)*mat*mat'
            mat2, mean2, normal2 = self.cpca(self.v2, 3,self.mesh2)  # obj0=obj2*mat'+mean2
        elif self.method=="npca":
            mat1, mean1, normal1 = self.npca(self.v1, 3,self.mesh1)  # obj0=(obj1-mean)*mat*mat'
            mat2, mean2, normal2 = self.npca(self.v2, 3,self.mesh2)  # obj0=obj2*mat'+mean2
        else: # pca
            mat1, mean1, normal1 = self.pca(self.v1, self.getDirect)  # obj0=(obj1-mean)*mat*mat'
            mat2, mean2, normal2 = self.pca(self.v2, self.getDirect)  # obj0=obj2*mat'+mean2
            
        m = mat1 * mat2.I
        y = mean2 - np.dot(mean1, m)

        m = np.array(m.tolist() + y.tolist())
        m = m.T.tolist() + [[0, 0, 0, 1]]
        return m, normal1.tolist(), normal2.tolist()
    @staticmethod
    def getDirect(v):#通过3次方判断朝向
        mean = np.mean(v, axis=0).tolist()[0]  # 这个均值理论上为[0,0,0]
        v = v.tolist()
        a = 1
        b = 1
        c = 1
        sum = [0, 0, 0]
        for vi in v:
            sum[0] = sum[0] + (vi[0] - mean[0]) ** 3
            sum[1] = sum[1] + (vi[1] - mean[1]) ** 3
            sum[2] = sum[2] + (vi[2] - mean[2]) ** 3
        if sum[0] == 0 or sum[1] == 0 or sum[2] == 0:
            print("检测到对称性:", sum)
        if sum[0] < 0:
            a = -1
        if sum[1] < 0:
            b = -1
        if sum[2] < 0:
            c = -1
        return np.array([
            [a, 0, 0],
            [0, b, 0],
            [0, 0, c]
        ])
    @staticmethod
    def getDirect2(v):#通过最远距离判断朝向
        import math
        mean = np.mean(v, axis=0).tolist()[0]  # 这个均值理论上为[0,0,0]
        v = v.tolist()
        furthest = [0, 0, 0] #距离坐标轴平面的最远距离
        for vi in v:
            for i in range(3):
                if abs(vi[i] - mean[i])>abs(furthest[i]):
                    furthest[i]=vi[i] - mean[i]
        if furthest[0] == 0 or furthest[1] == 0 or furthest[2] == 0:
            print("检测到对称性:", sum)
        a = 1
        b = 1
        c = 1
        if furthest[0] < 0:
            a = -1
        if furthest[1] < 0:
            b = -1
        if furthest[2] < 0:
            c = -1
        return np.array([
            [a, 0, 0],
            [0, b, 0],
            [0, 0, c]
        ])
    @staticmethod
    def orientation(x,y,z):
        if x>0:
            return 1
        elif x<0:
            return -1
        elif y>0:
            return 1
        elif y<0:
            return -1
        elif z<0:
            return -1
        else:
            return 1
    @staticmethod
    def getDirect3(redEigVects):#仅仅通过特征向量判断朝向 , 这种方式是错误的、在理解上的错误
        a=(redEigVects.T)[0].tolist()[0]
        b=(redEigVects.T)[1].tolist()[0]
        c=(redEigVects.T)[2].tolist()[0]

        f1=Alignment.orientation(a[0],a[1],a[2])
        f2=Alignment.orientation(b[0],b[1],b[2])
        f3=Alignment.orientation(c[0],c[1],c[2])
        return np.array([
            [f1, 0 , 0 ],
            [0 , f2, 0 ],
            [0 , 0 , f3]
        ])
    @staticmethod
    def pca(dataMat,getDirect):  
        topNfeat=3# topNfeat 降维后的维度
        # 去均值，将样本数据的中心点移到坐标原点
        meanVals = np.mean(dataMat, axis=0)  # 按列求均值，即每一列求一个均值，不同的列代表不同的特征
        meanRemoved = dataMat - meanVals  #

        # 计算协方差矩阵
        covMat = np.cov(meanRemoved, rowvar=0)

        # 计算协方差矩阵的特征值和特征向量
        # 确保方差最大  ，构造新特征两两独立
        eigVals, eigVects = np.linalg.eig(np.mat(covMat))
        eigValInd = np.argsort(eigVals)  # 排序,并获取排序后的下标 #sort, sort goes smallest to largest  #排序，将特征值按从小到大排列
        eigValInd = eigValInd[:-(topNfeat + 1):-1]  # cut off unwanted dimensions      #选择维度为topNfeat的特征值
        redEigVects = eigVects[:, eigValInd]  # reorganize eig vects largest to smallest   #选择与特征值对应的特征向量
        #print("redEigVects",redEigVects)

        direct = getDirect(meanRemoved * redEigVects)#direct = self.getDirect(meanRemoved * redEigVects)
        #direct = self.getDirect3(redEigVects)
        redEigVects = redEigVects * direct

        normalization = meanRemoved * redEigVects
        return redEigVects, meanVals, normalization
    @staticmethod
    def computeCovMat(dataMat):
        covMat=np.zeros([3,3])
        for v in dataMat:
            m=np.array([v])
            covMat=covMat+np.dot(m.T,m)
        return covMat
    @staticmethod
    def computeCovMat2(mesh):
        covMat=np.zeros([3,3])
        '''
        for i in range(len(mesh.face)):
            [v0,v1,v2],mid,s=mesh.getTriangle(i)
            m=np.array([v0])
            covMat=covMat+np.dot(m.T,m)*s
            m=np.array([v1])
            covMat=covMat+np.dot(m.T,m)*s
            m=np.array([v2])
            covMat=covMat+np.dot(m.T,m)*s
            m=np.array([mid])
            covMat=covMat+np.dot(m.T,m)*(s*9)
        '''
        for i in range(len(mesh.face)):
            [v0,v1,v2],mid,s=mesh.getTriangle(i)
            m=np.array([v0])
            covMat=covMat+np.dot(m.T,m)
            m=np.array([v1])
            covMat=covMat+np.dot(m.T,m)
            m=np.array([v2])
            covMat=covMat+np.dot(m.T,m)
            print(v0,v1,v2)
            print("v2",v2)
            print("mid",mid)
            #m=np.array([mid])
            #covMat=covMat+np.dot(m.T,m)
        
        #print("s<",covMat,">")
        return covMat
    @staticmethod
    def computeMean(mesh):
        areaAll=0
        mean0=np.array([0,0,0])
        data=[]
        for i in range(len(mesh.face)):
            [v0,v1,v2],m,s=mesh.getTriangle(i)
            data.append(m)
            mean0=mean0+np.array(m)*s
            areaAll=areaAll+s
        mean0=mean0/areaAll
        return mean0
        
    def cpca(self, dataMat, topNfeat,mesh):  # topNfeat 降维后的维度
        #covMat=self.computeCovMat2(mesh)
        #print(covMat)
        # 去均值，将样本数据的中心点移到坐标原点
        #meanVals=self.computeMean(mesh)     #均值
        meanVals = np.mean(dataMat, axis=0) 
        meanRemoved = dataMat - meanVals  #位置归一化
        
        # 计算协方差矩阵
        #covMat = np.cov(meanRemoved, rowvar=0)
        #covMat = self.computeCovMat2(mesh)
        covMat = self.computeCovMat(meanRemoved)

        # 计算协方差矩阵的特征值和特征向量
        # 确保方差最大  ，构造新特征两两独立
        eigVals, eigVects = np.linalg.eig(np.mat(covMat))
        eigValInd = np.argsort(eigVals)  # 排序,并获取排序后的下标 #sort, sort goes smallest to largest  #排序，将特征值按从小到大排列
        eigValInd = eigValInd[:-(topNfeat + 1):-1]  # cut off unwanted dimensions      #选择维度为topNfeat的特征值
        redEigVects = eigVects[:, eigValInd]  # reorganize eig vects largest to smallest   #选择与特征值对应的特征向量

        direct = self.getDirect(meanRemoved * redEigVects)
        redEigVects = redEigVects * direct

        normalization = meanRemoved * redEigVects
        return redEigVects, meanVals, normalization#使用cPCA后考虑的不仅仅是网格点
    def npca(self, dataMat, topNfeat,mesh):  # topNfeat 降维后的维度
        covMat=self.computeCovMat2(mesh)
        # 去均值，将样本数据的中心点移到坐标原点
        meanVals=self.computeMean(mesh)
        #meanVals = np.mean(dataMat, axis=0)  # 按列求均值，即每一列求一个均值，不同的列代表不同的特征
        meanRemoved = dataMat - meanVals  #
        
        # 计算协方差矩阵
        covMat = np.cov(meanRemoved, rowvar=0)

        # 计算协方差矩阵的特征值和特征向量
        # 确保方差最大  ，构造新特征两两独立
        eigVals, eigVects = np.linalg.eig(np.mat(covMat))
        eigValInd = np.argsort(eigVals)  # 排序,并获取排序后的下标 #sort, sort goes smallest to largest  #排序，将特征值按从小到大排列
        eigValInd = eigValInd[:-(topNfeat + 1):-1]  # cut off unwanted dimensions      #选择维度为topNfeat的特征值
        redEigVects = eigVects[:, eigValInd]  # reorganize eig vects largest to smallest   #选择与特征值对应的特征向量

        direct = self.getDirect2(meanRemoved * redEigVects)
        redEigVects = redEigVects * direct

        normalization = meanRemoved * redEigVects
        return redEigVects, meanVals, normalization#使用cPCA后考虑的不仅仅是网格点

if __name__ == "__main__":  # 用于测试
    import random
    mesh1 = Mesh('input/t1.obj')
    mesh1.rotation(random.random()*6.3, random.random()*6.3, random.random()*6.3)
    mesh1.move(random.random()*100-50, random.random()*100-50,random.random()*100-50)
    mesh1.download("output/mesh1.obj")

    mesh2 = mesh1.clone()
    mesh2.rotation(random.random()*6.3, random.random()*6.3, random.random()*6.3)
    mesh2.move(random.random()*100-50, random.random()*100-50,random.random()*100-50)
    mesh2.scale(-1,1,1)
    #mesh2 = Mesh('input/t2.obj')
    mesh2.download("output/mesh2.obj")

    align = Alignment(mesh1, mesh2)
    print("仿射变换矩阵为：\n", np.mat(align.mat))
    mesh1.applyMatrix(align.mat)
    mesh1.download("output/result.obj")

    mesh1.vertex = align.normal1
    mesh1.updateVertex()
    mesh1.download("output/mesh1_normal.obj")
    mesh2.vertex = align.normal2
    mesh2.updateVertex()
    mesh2.download("output/mesh2_normal.obj")
    #print(mesh1.getTriangle(0))
