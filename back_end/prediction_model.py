import sys
import csv
from sklearn import svm
import joblib
from numpy import *

# 读取文件中的数据
def loadTestData():
    l = []
    # sys.srgv[1]指的是传入的第一个参数
    with open(sys.argv[1]) as file:
        # csv.reader返回一个列表，每行是一个元素
        lines = csv.reader(file)
        for line in lines:
            l.append(line)
    # 去除表头
    l.remove(l[0])
    # 将列表变成numpy数组
    data = array(l)
    return nomalizing(toInt(data))


# 将数组转换为int类型
def toInt(array):
    # mat是numpy中的方法，将数组转换为矩阵，使用矩阵才能进行线性代数运算
    array = mat(array)
    # 获取行数和列数
    m, n = shape(array)
    # 构建一个新的矩阵，这个矩阵行数和列数与array相同，且全部填充0
    newArray = zeros((m,n))
    for i in range(m):
        for j in range(n):
            # 将array中的数值转换为int类型
            newArray[i][j] = int(array[i,j])
    return newArray


# 把非零的地方转为1  TODO: 为什么？？
def nomalizing(array):
    m,n = shape(array)
    for i in range(m):
        for j in range(n):
            if array[i,j] != 0:
                array[i,j] = 1


# 读取本次图像数据
testData = loadTestData()
# 读取训练模型
clf = joblib.load('./class_new_svmModel.pkl')
# 进行预测
testLable = clf.predict(testData)
print(testLable[0])