import numpy
a=numpy.array([
    [1,2,3],
    [4,5,6]
])
b=numpy.array([
    [9,0,3],
    [4,1,6]
])

# a=numpy.concatenate(a,b)
# a=numpy.concatenate(a,b)
a=numpy.vstack([a,b])
a=numpy.vstack([a,b])
print(a+2)
print(a.shape[0])