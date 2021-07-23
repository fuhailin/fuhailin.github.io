---
title: DeePray:深度学习推荐算法新基建
date: 2020-06-05 11:44:16
tags:
categories:
top:
---
开源项目 **DeePray** 发布啦！针对推荐算法，特别是点击率预估领域目不暇接的诞生新模型现状，如何将心仪模型快速应用于领域内一直是一项棘手的问题，DeePray这个项目通过统一构建数据流水线，提供各类网络层组件，在此之上，以模块化设计，用组件之砖，搭建各类网络之模型，并以灵活配置式的方式提供调用接口，你也可以在DeePray的基础上，选用各类组件模块，就像玩乐高积木一样建造你自己的模型。`deepray.model`目录下已实现LR、FM、FFM、DeepFM、Wide&Deep、Deep&Cross、NFM、xDeepFM、FLEN、AutoInt、DIN等各具特色的分类模型，你只需要处理好自己的数据，然后`import deepray as dp`就可以使用啦！

总之DeePray的目标是：

 - 容易使用, 即使新手也可以快速上手深度学习工具
 - 面对大规模数据也能快速处理
 - 易于扩展的模块化架构可以像玩乐高游戏一样构建神经网络！

<!-- more -->

由于开始动手做这个项目的时候是在2020年1月份左右，那时候TensorFlow 2.0正式版已经推出3个月了，而TensorFlow1.x静态图运行和TensorFlow2.x默认动态图运行方式让TensorFlow的使用就像两套不同的语言，于是我选择向前看直接从TensorFlow 2.0开始，边学习TF2的使用边开始DeePray的开发，历时半年的业余时间，中间又经历了两次TensorFlow正式版的升级，因此你在使用DeePray时候需要保证已经安装了最新版本的TensorFlow（TensorFlow>=2.2.0）。

DeePray的诞生免不了与另一个前辈DeepCTR进行比较，DeePray具有比DeepCTR更高的模块复用结构，因此也更加容易扩展。
以Deep&Cross模型为例，这是一个典型的双塔结构网络，Deep网络和Cross网络是并行的，Embedding层和Prediction层等公共网络层已抽取到父类BaseCTRModel中，因此新的个性化模型只需继承BaseCTRModel，然后从deepray.base.layers中选用组件DeepNet和CrossNet就可以搭建Deep&Cross网络了，是不是就跟搭建积木一样简单。

| DeePray                                                      | DeepCTR                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![Screen Shot 2020-06-05 at 4.01.39 PM](https://pic2.zhimg.com/80/v2-e99820394041aff5f3acd64817d4d621_1440w.jpg) | ![Screen Shot 2020-06-05 at 3.56.01 PM](https://pic1.zhimg.com/80/v2-e1caf0a921c5bfb4b0e06e2cee55c2dc_1440w.jpg) |
| ![Screen Shot 2020-06-05 at 4.40.30 PM](https://pic3.zhimg.com/80/v2-6ff7a6a39918c4bc023fcd42207fb32a_1440w.jpg) | ![Screen Shot 2020-06-05 at 4.41.04 PM](https://pic4.zhimg.com/80/v2-5965510232fe17c5cf1824b72ac40c77_1440w.jpg) |


分别由DeePray和DeepCTR实现的DCN、DeepFM模型对比，窃以为DeePray中的实现更为简洁、也更为清晰易读。在一个个实现不同网络模型的过程中，我也参考了DeepCTR的实现方案，在此向浅梦大佬致敬！

# Data Pipeline

面对海量的多到内存一次放不下的数据，构建数据流水线是一个好主意，因此DeePray选择与TensorFlow的DataSet api深度整合，支持TFRecords数据格式，通过调整数据读取相关参数以便获得最佳性能，当然你也可以继承`BaseCTRModel`类后重写`create_train_data_iterator()`方法来构造自己的数据迭代器，下面以Census Adult Data Set为例，进行数据处理准备DeePray的输入数据

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

from deepray.utils.converter import CSV2TFRecord


# http://archive.ics.uci.edu/ml/datasets/Adult
train_data = 'DeePray/examples/census/data/raw_data/adult_data.csv'
df = pd.read_csv(train_data)
df['income_label'] = (df["income_bracket"].apply(lambda x: ">50K" in x)).astype(int)
df.pop('income_bracket')

NUMERICAL_FEATURES = ['age', 'fnlwgt', 'hours_per_week', 'capital_gain', 'capital_loss', 'education_num']
CATEGORY_FEATURES = [col for col in df.columns if col != LABEL and col not in NUMERICAL_FEATURES]
LABEL = ['income_label']

for feat in CATEGORY_FEATURES:
    lbe = LabelEncoder()
    df[feat] = lbe.fit_transform(df[feat])
# Feature normilization
mms = MinMaxScaler(feature_range=(0, 1))
df[NUMERICAL_FEATURES] = mms.fit_transform(df[NUMERICAL_FEATURES])


prebatch = 1  # flags.prebatch
converter = CSV2TFRecord(LABEL, NUMERICAL_FEATURES, CATEGORY_FEATURES, VARIABLE_FEATURES=[], gzip=False)
converter.write_feature_map(df, './data/feature_map.csv')

train_df, valid_df = train_test_split(df, test_size=0.2)
converter(train_df, out_file='./data/train.tfrecord', prebatch=prebatch)
converter(valid_df, out_file='./data/valid.tfrecord', prebatch=prebatch)
```

# 快速实验

完成数据预处理之后通过简单的几行代码，填写好必要配置之后便可进行试验，如果你想换用其他模型，只需修改`--model`一个参数即可

```python
import sys

from absl import app, flags

import deepray as dp
from deepray.base.trainer import train
from deepray.model.build_model import BuildModel

FLAGS = flags.FLAGS

def main(flags=None):
    FLAGS(flags, known_only=True)
    flags = FLAGS
    model = BuildModel(flags)
    history = train(model)
    print(history)

argv = [
    '--model=lr',
    '--train_data=/Users/vincent/Projects/DeePray/examples/census/data/train',
    '--valid_data=/Users/vincent/Projects/DeePray/examples/census/data/valid',
    '--feature_map=/Users/vincent/Projects/DeePray/examples/census/data/feature_map.csv',
    '--learning_rate=0.01',
    '--epochs=10',
    '--batch_size=64',
]
main(flags=argv)
```

# 构建个性化新网络模型

只需要继承`BaseCTRModel`类，然后在`build`方法中选用你想要的网络组件，既可以是Keras中已有的、也可以是deepray.base.layers中提供的，还可以是你自己创造的.

```python
class CustomModel(BaseCTRModel):
    def build(self, input_shape):
        self.lstm_block = tf.keras.layers.LSTM(50)

    def build_network(self, features, is_training=None):
        v = self.lstm_block(features)
        return v
```

# 开始尝试吧

目前DeePray的安装包已托管到pypi，只需要`pip install deepray`就可以快速安装，具体的CPU或GPU运行设备是由你的TensorFlow版本决定的，记住DeePray要配合最新的TensorFlow版本使用喔！

DeePray这个项目还在持续开发中，新模型的开发、测试、文档，包括可能的PyTorch版本都需要补充，目前我个人精力有限，迭代会不及时，特别欢迎感兴趣的同学参与进来一起完善建设和维护！快来点个Star吧！

https://github.com/fuhailin/DeePray

# 题外记

2020年春节，突然爆发的病毒疫情，让我和父母在湖北家中整整隔离了近60天没有出门，这也迫使我有时间完成DeePray基础搭建工作，谨以此文纪念那段特殊时光。



最后我也开通了微信公众号【公众号ID：StateOfTheArt】，欢迎大家关注一起交流！

![关注公众号趙大寳Note](https://gitee.com/fuhailin/Object-Storage-Service/raw/master/wechat_channel.png)