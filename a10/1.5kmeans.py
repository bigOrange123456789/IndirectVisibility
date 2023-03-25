print("基于构件的可见特征对构件进行分块聚类")
######################################
import numpy as np
import random
import math
list1 = [1, 2, 3, 4, 5]  
list1 = [
    [0,0],
    [0,100],
    [0,10000],
    [0,0],
    [0,100],

    [0,10000],
    [0,0],
    [0,100],
    [0,10000],
    [0,0],

    [0,100],
    [0,10000],
    [0,0],
    [0,100],
    [0,10000],
]  
print(random.sample(list1,3))
# exit(0)

def k_means(data, k, batch_size, max_iter=100):
    n = len(data)
    # 随机选取k个中心点
    
    centers = random.sample(data.tolist(), k)
    # 初始化聚类结果
    clusters = [[] for i in range(k)]
    # 初始化迭代次数
    iter = 0
    
    while iter < max_iter:
        # 分批读取数据
        for i in range(math.ceil(n / batch_size)):
            batch_data = data[i*batch_size:(i+1)*batch_size]
            # 将数据点分配到最近的中心点
            for point in batch_data:
                distances = [np.linalg.norm(point - center) for center in centers]
                cluster_idx = np.argmin(distances)
                clusters[cluster_idx].append(point)

            # 计算新的中心点
            new_centers = []
            for i in range(k):
                new_center = np.mean(clusters[i], axis=0)
                new_centers.append(new_center)

            # # 判断是否达到收敛条件
            # if np.allclose(centers, new_centers):
            #     break

            # 更新中心点
            centers = new_centers
            # 重置聚类结果
            clusters = [[] for i in range(k)]

        iter += 1
    
    return centers, clusters

####################
data=[
    [0,0],
    [0,100],
    [0,10000],
    [0,0],
    [0,100],

    [0,10000],
    [0,0],
    [0,100],
    [0,10000],
    [0,0],

    [0,100],
    [0,10000],
    [0,0],
    [0,100],
    [0,10000],
]
data=np.array(data)
k=3
batch_size=15
centers, clusters=k_means(data, k, batch_size, max_iter=100)
print("centers", centers)
print("clusters",clusters)