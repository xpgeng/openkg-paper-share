
## Interaction Embeddings for Prediction and Explanation

> 笔记整理：张文，浙江大学在读博士，研究方向为知识图谱的表示学习，推理和可解释。

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_1.png)

本文是我们与苏黎世大学合作的工作，将发表于WSDM2019，这篇工作在知识图谱的表示学习中考虑了实体和关系的交叉交互，并且从预测准确性和可解释性两个方面评估了表示学习结果的好坏。

 

给定知识图谱和一个要预测的三元组的头实体和关系，在预测尾实体的过程中，头实体和关系之间是有交叉交互的crossoverinteraction, 即关系决定了在预测的过程中哪些头实体的信息是有用的，而对预测有用的头实体的信息又决定了采用什么逻辑去推理出尾实体，文中通过一个模拟的知识图谱进行了说明如下图所示：

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_2.png)

基于对头实体和关系之间交叉交互的观察，本文提出了一个新的知识图谱表示学习模型CrossE. CrossE除了学习实体和关系的向量表示，同时还学习了一个交互矩阵C，C与关系相关，并且用于生成实体和关系经过交互之后的向量表示，所以在CrossE中实体和关系不仅仅有通用向量表示，同时还有很多交互向量表示。CrossE核心想法如下图：

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_3.png)

在CrossE中，头实体的向量首先和交互矩阵作用生成头实体的交互表示，然后头实体的交互表示和关系作用生成关系的交互表示，最后头实体的交互表示和关系的交互表示参与到具体的三元组计算过程。对于一个三元组的计算过程展开如下：

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_4.png)

实验中本文首先用链接预测的效果衡量了表示学习的效果，实验采用了三个数据集WN18， FB15k,FB15k-237, 实验结果如下：

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_5.png)

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_6.png)

从实验结果中我们可以看出，CrossE实现了较好的链接预测结果。我们去除CrossE中的头实体和关系的交叉交互，构造了模型 CrossE<sub>S</sub>，CrossE 和 CrossE<sub>S</sub> 的比较说明了交叉交互的有效性。

 

除了链接预测，我们还从一个新的角度评估了表示学习的效果，即可解释性。我们提出了一种基于相似结构通过知识图谱的表示学习结果生成预测结果解释的方法，并提出了两种衡量解释结果的指标，AvgSupport和Recall。Recall是指模型能给出解释的预测结果的占比，其介于0和1之间且值越大越好；AvgSupport是模型能给出解释的预测结果的平均support个数，AvgSupport是一个大于0的数且越大越好。可解释的评估结果如下：

![](img/Interaction-Embeddings-for-Prediction-and-Explanation.md_7.png)

从实验结果中我们可以看出，整体来说CrossE能够更好地对预测结果生成解释。

 

链接预测和可解释的实验从两个不同的方面评估了知识图谱表示学习的效果，同时也说明了链接预测的准确性和可解释性没有必然联系，链接预测效果好的模型并不一定能够更好地提供解释，反之亦然。
