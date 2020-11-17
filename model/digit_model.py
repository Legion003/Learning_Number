# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author Legion
@date 2020/11/15 20:32
@description 使用CNN进行数字识别，使用pytorch包
"""
import numpy as np
import csv
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset


def load_data(proportion):
    """
    读取原始数据，根据比例划分训练集和测试集
    :param proportion: 训练集与测试集的比例
    :return: 训练集输入， 训练集期望输出， 测试集输入， 测试集期望输出
    """
    l = []
    # 读取数据
    with open('tmp_img_encode.txt', 'r') as fp:
        lines = csv.reader(fp)
        for line in lines:
            l.append(line)
    # 去掉行头
    l.remove(l[0])
    # 转为numpy数组，控制元素的类型为uint8
    l = np.array(l, dtype=np.uint8)
    m, n = np.shape(l)
    # 根据比例计算训练集和测试集的样本大小
    train_size = int((m/(proportion+1))*proportion)
    test_size = m - train_size
    # 提取输入数据
    train_data = l[0:train_size, 1:]
    train_data = np.reshape(train_data, (train_size, 28, 28, 1))
    test_data = l[train_size:m, 1:]
    test_data = np.reshape(test_data, (test_size, 28, 28, 1))
    # 提取label（期望输出）
    train_dest = l[0:train_size, 0]
    test_dest = l[train_size:m, 0]
    return train_data, train_dest, test_data, test_dest


class ImgDataset(Dataset):
    """
    使用Dataset包装数据
    """
    def __init__(self, x, y=None, transform=None):
        self.x = x
        self.y = y
        # label需要被设置为LongTensor
        if y is not None:
            self.y = torch.LongTensor(y)
        self.transform = transform

    def __len__(self):
        """
        Dataset要求重写的方法
        :return: Dataset的大小
        """
        return len(self.x)

    def __getitem__(self, index):
        """
        Dataset要求重写的方法
        定义当使用[]取值时要返回什么数据
        :param index: 索引
        :return: x(, y)
        """
        X = self.x[index]
        if self.transform is not None:
            X = self.transform(X)
        if self.y is not None:
            Y = self.y[index]
            return X, Y
        return X


class Classifier(nn.Module):
    """
    CNN模型搭建
    过程：卷积 -> 池化 -> 卷积 -> 池化 -> 全连接
    """
    def __init__(self):
        super(Classifier, self).__init__()
        # torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding)
        # torch.nn.MaxPool2d(kernel_size, stride, padding)
        self.cnn = nn.Sequential(
            nn.Conv2d(1, 14, 3, 1, 1),  # (14, 28, 28)
            # 归一化
            nn.BatchNorm2d(14),
            # 激活函数，将小于0的元素变为0
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0),  # (14, 14, 14)
            nn.Conv2d(14, 28, 3, 1, 1),  # (28, 14, 14)
            nn.BatchNorm2d(28),
            nn.ReLU(),
            nn.MaxPool2d(2, 2, 0)  # (28, 7, 7)
        )
        # 全连接
        self.fc = nn.Sequential(
            nn.Linear(28*7*7, 10)
        )

    def forward(self, x):
        out = self.cnn(x)
        # 将cnn的结果拉直
        out = out.view(out.size()[0], -1)
        return self.fc(out)


if __name__ == '__main__':
    (train_data, train_dest, test_data, test_dest) = load_data(4)
    # 设置预处理方法
    transform = transforms.Compose([
        # 转为PIL图像
        transforms.ToPILImage(),
        # 转为tensor
        transforms.ToTensor()
    ])
    batch_size = 10
    train_set = ImgDataset(train_data, train_dest, transform)
    test_set = ImgDataset(test_data, test_dest, transform)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

    # 使用显卡进行计算
    model = Classifier().cuda()
    # 设定交叉熵为损失函数
    loss = nn.CrossEntropyLoss()
    # 设定最优化方法，参数为模型中的参数和学习速率
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    # 迭代次数
    num_epoch = 30

    for epoch in range(num_epoch):
        model.train()
        for i, data in enumerate(train_loader):
            # 将梯度归零
            optimizer.zero_grad()
            # 相当于调用model中的forward函数
            train_pred = model(data[0].cuda())
            # 计算loss
            batch_loss = loss(train_pred, data[1].cuda())
            # 计算梯度
            batch_loss.backward()
            # 更新参数
            optimizer.step()

    # 锁住权值，不让权值变动
    model.eval()
    test_result = []
    # 使用模型进行预测
    with torch.no_grad():
        for i, data in enumerate(test_loader):
            test_pred = model(data[0].cuda())
            test_pred = np.argmax(test_pred.cpu().data.numpy(), axis=1)
            for y in test_pred:
                test_result.append(y)
    test_result = np.array(test_result, dtype=np.uint8)

    # 计算准确率
    test_size = np.size(test_result)
    err = 0
    for i in range(test_size):
        if test_result[i] != test_dest[i]:
            err = err + 1
    precision = (test_size-err) / test_size
    print(precision)

    # # 保存网络和参数
    # torch.save(model, './cnn_model.pkl')



