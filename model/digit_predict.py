# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author Legion
@date 2020/11/16 23:26
@description 读取数字图片，使用已经做好的模型进行识别
"""

import sys
import numpy as np
import csv
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset


def load_data(path):
    """
    读取图片数据
    """
    l = []
    with open(path, 'r') as fp:
        lines = csv.reader(fp)
        for line in lines:
            l.append(line)
    l.remove(l[0])
    data = np.array(l, dtype=np.uint8)
    data = np.reshape(data, (1, 28, 28, 1))
    return data


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


# 读取model
model = torch.load('./cnn_model.pkl')
model.eval()
# 读取数据
path = sys.argv[1]
input_data = load_data(path)

transform = transforms.Compose([
        # 转为PIL图像
        transforms.ToPILImage(),
        # 转为tensor
        transforms.ToTensor()
    ])
data_set = ImgDataset(input_data, transform=transform)
data_loader = DataLoader(data_set, batch_size=1, shuffle=False)
# 进行识别
with torch.no_grad():
    for i, data in enumerate(data_loader):
        prediction = model(data.cuda())
        prediction = np.argmax(prediction.cpu().data.numpy(), axis=1)
        print(prediction)

