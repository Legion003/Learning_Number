#!/bin/bash
# 本脚本用于分析用户写的是什么数字

# 运行java文件将图片灰度化
java getRGB ./images/number.png > ./data/img_code.txt
if [ $? -eq 0 ]
then
    echo "s"
    # # 运行python文件对图片进行分析，最后得出一个数字结果
    # num=$(python3 .back_end/prediction_model.py ../data/img_code.txt)
    # # 返回这个结果
    # echo $num
else
    echo "null"
fi