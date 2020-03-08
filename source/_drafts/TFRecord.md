---
title: TFRecord ：TensorFlow 数据集存储格式
tags: TF
categories:
top:
---
TFRecord 是 TensorFlow 特有的的二进制数据集存储格式。当我们将数据集整理成 TFRecord 格式后，TensorFlow 就可以高效地读取和处理这些数据集，从而帮助我们更高效地进行大规模的数据训练。
<!-- more -->

二进制数据可以占用更少的磁盘空间、花费更少的复制时间、读取也更加高效，特别是当你使用的是机械硬盘时，这些特性比在SSD上更加明显。

[TFRecord ：TensorFlow 数据集存储格式](https://tf.wiki/zh/basic/tools.html#tfrecord-tensorflow)
[TFRecord and tf.Example](https://www.tensorflow.org/tutorials/load_data/tfrecord)
[TensorFlow的tfrecords文件详解](https://mp.weixin.qq.com/s/FIffvAzyHSaijjyv7yfZcw)

写入文件TFRecord
